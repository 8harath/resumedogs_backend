import os
import logging
from typing import Tuple
from fastapi import HTTPException, status
import anyio
from latex_utils import (
    write_latex_to_file,
    build_pdflatex_command,
    run_pdflatex_command,
    read_pdf_file,
    get_pdf_and_tex_filenames,
    format_pdflatex_error
)

logger = logging.getLogger(__name__)

async def convert_latex_to_pdf(latex_content: str) -> Tuple[bytes, str]:
    """
    Converts LaTeX content to a PDF file using pdflatex.
    Ignores pdflatex errors if PDF is successfully generated.
    Runs pdflatex in a thread pool to avoid blocking the event loop.
    
    Args:
        latex_content: String containing valid LaTeX code
        
    Returns:
        Tuple[bytes, str]: PDF content and filename
    """
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.getcwd(), 'latex_output')
        os.makedirs(output_dir, exist_ok=True)
        
        tex_path = write_latex_to_file(latex_content, output_dir)
        pdf_filename, pdf_path = get_pdf_and_tex_filenames(tex_path)
        pdflatex_cmd = build_pdflatex_command(tex_path, output_dir)
        logger.info(f"Executing pdflatex command: {' '.join(pdflatex_cmd)}")

        def sync_pdflatex():
            return run_pdflatex_command(pdflatex_cmd, output_dir)
        process = await anyio.to_thread.run_sync(sync_pdflatex)

        # Log any errors but don't raise exception
        if process.returncode != 0:
            logger.warning(f"pdflatex returned non-zero code: {process.returncode}")
            logger.error(f"STDERR: {process.stderr}")

        # Check if PDF was generated despite errors
        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
            # Read the PDF content
            pdf_content = read_pdf_file(pdf_path)
            logger.info(f"Successfully generated PDF: {pdf_filename} ({len(pdf_content)} bytes)")
            return pdf_content, pdf_filename
        else:
            # Include last 20 lines of pdflatex stderr in the error detail for easier debugging
            last_stderr = format_pdflatex_error(process.stderr)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"PDF generation failed - output file not found or empty. pdflatex stderr (last 20 lines):\n{last_stderr}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during LaTeX to PDF conversion: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to convert LaTeX to PDF: {str(e)}"
        )