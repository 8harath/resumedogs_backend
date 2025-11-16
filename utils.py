# /backend/utils.py
import io
import logging
from fastapi import UploadFile, HTTPException

# File parsing imports
import docx # python-docx
import fitz  # PyMuPDF for PDF extraction

logger = logging.getLogger(__name__)

async def extract_text_from_file(file: UploadFile) -> str:
    """
    Extracts text and hyperlinks from UploadFile (PDF, DOCX, MD/TXT).

    Args:
        file: The uploaded file object from FastAPI.

    Returns:
        A string with extracted text and hyperlinks.

    Raises:
        HTTPException: If the file type is unsupported or parsing fails.
    """
    filename = file.filename or "unknown_file"
    content_type = file.content_type
    logger.info(f"Attempting to extract text from file: {filename} (Type: {content_type})")

    # Limit file size (e.g., 10MB) - Optional but recommended
    MAX_FILE_SIZE = 10 * 1024 * 1024
    content = await file.read()  # Read file content async
    size = len(content)
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File size exceeds limit ({MAX_FILE_SIZE / 1024 / 1024} MB).")
    await file.seek(0) # Go back to start if you need to re-read

    try:
        content = await file.read() # Read file content async
        if not content:
             logger.warning(f"File {filename} appears to be empty.")
             # Decide if empty file is error or just returns empty string
             raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        text = ""
        hyperlinks = []
        if content_type == 'application/pdf' or filename.lower().endswith(".pdf"):
            try:
                with io.BytesIO(content) as pdf_file:
                    pdf_file.seek(0)
                    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
                    for page_num in range(len(doc)):
                        page = doc[page_num]
                        # Extract text
                        text += page.get_text("text") + "\n"
                        # Extract hyperlinks
                        links = page.get_links()
                        for link in links:
                            if link.get("uri"):
                                rect = link.get("from")
                                link_text = ""
                                if rect:
                                    words = page.get_text("words")
                                    for w in words:
                                        x0, y0, x1, y1, word = w[:5]
                                        if x0 >= rect.x0 and x1 <= rect.x1 and y0 >= rect.y0 and y1 <= rect.y1:
                                            link_text += word + " "
                                    link_text = link_text.strip()
                                hyperlinks.append(f"Page {page_num + 1}: '{link_text}' -> {link['uri']}")
            except Exception as pdf_err:
                logger.error(f"Error reading PDF content from {filename}: {pdf_err}", exc_info=True)
                raise HTTPException(status_code=400, detail=f"Could not parse PDF file: {pdf_err}")
            logger.info(f"Successfully extracted {len(text)} characters and {len(hyperlinks)} hyperlinks from PDF: {filename}")
            if hyperlinks:
                text += "\n\nHyperlinks found in PDF:\n" + "\n".join(hyperlinks)
            return text


        elif content_type in [
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/msword'
        ] or filename.lower().endswith((".docx", ".doc")):
            # Handle both DOCX and DOC
            try:
                if filename.lower().endswith(".docx"):
                    with io.BytesIO(content) as docx_file:
                        document = docx.Document(docx_file)
                        for para in document.paragraphs:
                            text += para.text + "\n"
                else:
                    # For .doc files, try using textract if available
                    import subprocess
                    import tempfile
                    with tempfile.NamedTemporaryFile(delete=True, suffix='.doc') as tmp:
                        tmp.write(content)
                        tmp.flush()
                        try:
                            # Try textract first
                            import textract
                            extracted = textract.process(tmp.name)
                            text += extracted.decode('utf-8', errors='replace')
                        except ImportError:
                            # Fallback to antiword if textract is not installed
                            try:
                                result = subprocess.run([
                                    'antiword', tmp.name
                                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                                text += result.stdout.decode('utf-8', errors='replace')
                            except Exception as antiword_err:
                                logger.error(f"Error using antiword for DOC file {filename}: {antiword_err}", exc_info=True)
                                raise HTTPException(status_code=400, detail=f"Could not parse DOC file: {antiword_err}")
            except Exception as doc_err:
                logger.error(f"Error reading Word content from {filename}: {doc_err}", exc_info=True)
                raise HTTPException(status_code=400, detail=f"Could not parse Word file: {doc_err}")
            logger.info(f"Successfully extracted {len(text)} characters from Word file: {filename}")
            return text


        elif content_type in ['text/markdown', 'text/plain'] or filename.lower().endswith((".md", ".txt")):
             try:
                 # Try decoding as UTF-8, add fallback if needed
                 text = content.decode('utf-8')
             except UnicodeDecodeError:
                 try:
                     # Fallback to latin-1 or another common encoding if UTF-8 fails
                     logger.warning(f"UTF-8 decoding failed for {filename}, trying latin-1.")
                     text = content.decode('latin-1')
                 except Exception as decode_err:
                     logger.error(f"Failed to decode text file {filename}: {decode_err}", exc_info=True)
                     raise HTTPException(status_code=400, detail="Could not decode text file. Ensure it's UTF-8 encoded.")
             logger.info(f"Successfully extracted {len(text)} characters from Text/Markdown: {filename}")
             return text

        else:
            logger.warning(f"Unsupported file type: {content_type} for file {filename}")
            raise HTTPException(
                status_code=415, # Unsupported Media Type
                detail=f"Unsupported file type: '{content_type}'. Please upload PDF, DOCX, MD, or TXT."
            )

    except HTTPException:
        raise # Re-raise HTTP exceptions directly
    except Exception as e:
        logger.error(f"Failed to read or parse file {filename}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file {filename}. Please try again or contact support."
        )