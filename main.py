# /backend/main.py
import os
import sys
import logging
import time
import json

from fastapi import (
    FastAPI,
    File,
    UploadFile,
    Form,
    HTTPException,
    Depends,
    Request,
    Header,
    status,
    Response,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Import from project modules
from models import (
    TailoredResumeResponse,
    User,
    MessageResponse,
    ResumeData,
    JsonToLatexResponse,
)
from utils import extract_text_from_file
from resume_processor import (
    setup_resume_tailoring_chain,
    generate_tailored_resume,
    generate_latex_resume,
)
from auth import bearer_scheme
from latex_converter import convert_latex_to_pdf
from auth_utils import get_user_id_from_jwt
from usage import check_user_usage_limits, increment_user_usage
from supabase_utils import upload_pdf_to_bucket, insert_resume_record
from email_service import send_resume_conversion_notification
import shutil

# --- Initial Setup ---

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# --- Initialize LangChain Chains (on startup) ---
resume_tailoring_chain = None
latex_conversion_chain = None

try:
    logger.info("Setting up LangChain chains on application startup...")
    resume_tailoring_chain, latex_conversion_chain = setup_resume_tailoring_chain(
        model_name=None  # Set model name here
    )
    logger.info("LangChain chains setup complete.")
except Exception as e:
    logger.critical(
        f"FATAL: Failed to initialize LangChain chains on startup: {e}", exc_info=True
    )
    sys.exit(f"Startup failed: Could not initialize LangChain: {e}")

# --- FastAPI Application Instance ---
app = FastAPI(
    title="AI Resume Tailoring API",
    description="Tailors resumes based on job descriptions using AI.",
    version="0.2.0",
)

# --- CORS Middleware ---
origins = ["*"]  # Configure allowed origins here

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---


@app.get("/health", tags=["Status"], response_model=MessageResponse)
async def health_check():
    """Simple health check endpoint."""
    return {"message": "API is running!"}


@app.post("/tailor", tags=["Resume"], response_model=TailoredResumeResponse)
async def tailor_resume_endpoint(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    job_description: str = Form(
        ..., min_length=50, description="The full text of the job description."
    ),
    resume_file: UploadFile = File(
        ..., description="The user's resume file (PDF, DOCX, MD, TXT)."
    ),
):
    """
    Receives a job description and a resume file, tailors the resume,
    and returns the result.
    """
    # Extract user_id from JWT
    user_id = get_user_id_from_jwt(credentials)
    logger.info(f"Request from user_id: {user_id}")

    # Check usage limits
    daily, monthly = check_user_usage_limits(user_id)
    daily_current_str = (
        str(daily.current_usage) if hasattr(daily, "current_usage") else str(daily)
    )
    daily_limit_str = str(daily.limit) if hasattr(daily, "limit") else "N/A"
    monthly_current_str = (
        str(monthly.current_usage)
        if hasattr(monthly, "current_usage")
        else str(monthly)
    )
    monthly_limit_str = str(monthly.limit) if hasattr(monthly, "limit") else "N/A"
    logger.info(
        f"User usage: Daily={daily_current_str}/{daily_limit_str}, Monthly={monthly_current_str}/{monthly_limit_str}"
    )

    start_time = time.time()
    logger.info(f"Received tailor request for file '{resume_file.filename}'.")

    if not resume_file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Filename cannot be empty."
        )

    try:
        original_resume_text = await extract_text_from_file(resume_file)
        logger.info(
            f"Extracted {len(original_resume_text)} chars from '{resume_file.filename}'."
        )

        if not resume_tailoring_chain:
            logger.critical("Resume tailoring chain is not available.")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Resume processing service temporarily unavailable.",
            )

        modified_resume_text = await generate_tailored_resume(
            resume_content=original_resume_text,
            job_description=job_description,
            chain=resume_tailoring_chain,
        )
        logger.info(f"Successfully generated tailored resume.")

        end_time = time.time()
        processing_time_ms = (end_time - start_time) * 1000
        logger.info(f"Request completed in {processing_time_ms:.2f} ms.")

        # Increment usage counters
        increment_user_usage(user_id, daily, monthly)

        return TailoredResumeResponse(
            filename=resume_file.filename,
            original_content_length=len(original_resume_text),
            job_description_length=len(job_description),
            tailored_resume_text=modified_resume_text,
        )

    except HTTPException as he:
        raise he
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except RuntimeError as re:
        logger.error(f"Runtime error during processing: {re}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re)
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )


@app.post("/convert-latex", tags=["Resume"])
async def convert_to_latex_endpoint(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    resume_file: UploadFile = File(
        ..., description="The user's resume file (PDF, DOCX, MD, DOC)."
    ),
) -> Response:
    """
    Converts a resume file to LaTeX format and returns a compiled PDF.
    Adds JWT authentication, user usage limit check, and removes Stripe dependencies.
    """
    # Extract user_id from JWT
    user_id = get_user_id_from_jwt(credentials)
    # Check usage limits
    daily, monthly = check_user_usage_limits(user_id)
    daily_current_str = (
        str(daily.current_usage) if hasattr(daily, "current_usage") else str(daily)
    )
    daily_limit_str = str(daily.limit) if hasattr(daily, "limit") else "N/A"
    monthly_current_str = (
        str(monthly.current_usage)
        if hasattr(monthly, "current_usage")
        else str(monthly)
    )
    monthly_limit_str = str(monthly.limit) if hasattr(monthly, "limit") else "N/A"
    logger.info(
        f"User usage: Daily={daily_current_str}/{daily_limit_str}, Monthly={monthly_current_str}/{monthly_limit_str}"
    )

    # Parse file and convert to LaTeX
    try:
        if not resume_file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename cannot be empty.",
            )
        if not resume_file.filename.lower().endswith((".pdf", ".md", ".docx", ".doc")):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF, Markdown (.md), DOCX, and DOC files are supported.",
            )
        original_resume_text = await extract_text_from_file(resume_file)
        latex_resume_text = await generate_latex_resume(
            resume_content=original_resume_text, chain=latex_conversion_chain
        )
        pdf_content, pdf_filename = await convert_latex_to_pdf(latex_resume_text)

        # Upload PDF to Supabase bucket and get public link
        local_pdf_path = os.path.join(os.getcwd(), "latex_output", pdf_filename)
        public_url = upload_pdf_to_bucket(local_pdf_path, pdf_filename)

        # Insert record into resume_table
        insert_resume_record(public_url, user_id)

        # Send email notification
        try:
            email_sent = await send_resume_conversion_notification(
                credentials=credentials,
                resume_link=public_url,
                conversion_type="resume"
            )
            if email_sent:
                logger.info(f"Email notification sent to user {user_id}")
            else:
                logger.warning(f"Failed to send email notification to user {user_id}")
        except Exception as email_error:
            logger.error(f"Error sending email notification: {email_error}")
            # Don't fail the main request if email fails

        # Clean up only files related to this PDF conversion
        latex_output_dir = os.path.join(os.getcwd(), "latex_output")
        base_name, _ = os.path.splitext(pdf_filename)
        for ext in [".pdf", ".tex", ".aux", ".log", ".out"]:
            file_path = os.path.join(latex_output_dir, f"{base_name}{ext}")
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as cleanup_err:
                logger.warning(f"Failed to delete {file_path}: {cleanup_err}")

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in convert-latex endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    # Increment usage counters
    increment_user_usage(user_id, daily, monthly)
    daily_log_val = "N/A"
    if (
        hasattr(daily, "current_usage")
        and getattr(daily, "current_usage", None) is not None
    ):
        daily_log_val = str(daily.current_usage + 1)
    elif isinstance(daily, int):
        daily_log_val = str(daily + 1)

    monthly_log_val = "N/A"
    if (
        hasattr(monthly, "current_usage")
        and getattr(monthly, "current_usage", None) is not None
    ):
        monthly_log_val = str(monthly.current_usage + 1)
    elif isinstance(monthly, int):
        monthly_log_val = str(monthly + 1)
    logger.info(
        f"Incremented usage for user {user_id}. New usage: Daily={daily_log_val}, Monthly={monthly_log_val}"
    )

    return {"resume_link": public_url}


@app.post("/convert-json-to-latex", tags=["Resume"], response_model=JsonToLatexResponse)
async def convert_json_to_latex_endpoint(
    resume_data: ResumeData,  # Expect ResumeData model as request body
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> JsonToLatexResponse:
    """
    Converts structured JSON resume data to LaTeX format and returns a compiled PDF.
    Requires JWT authentication and tracks user usage.
    """
    start_time = time.time()
    logger.info("Received convert-json-to-latex request.")

    # Extract user_id from JWT
    user_id = get_user_id_from_jwt(credentials)
    logger.info(f"Request from user_id: {user_id}")

    # Check usage limits
    daily, monthly = check_user_usage_limits(user_id)
    daily_current_str = (
        str(daily.current_usage) if hasattr(daily, "current_usage") else str(daily)
    )
    daily_limit_str = str(daily.limit) if hasattr(daily, "limit") else "N/A"
    monthly_current_str = (
        str(monthly.current_usage)
        if hasattr(monthly, "current_usage")
        else str(monthly)
    )
    monthly_limit_str = str(monthly.limit) if hasattr(monthly, "limit") else "N/A"
    logger.info(
        f"User usage: Daily={daily_current_str}/{daily_limit_str}, Monthly={monthly_current_str}/{monthly_limit_str}"
    )

    if not latex_conversion_chain:
        logger.critical("LaTeX conversion chain is not available.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Resume processing service temporarily unavailable.",
        )

    try:
        # Convert Pydantic model to JSON string to be used as resume_content
        # The LATEX_CONVERSION_PROMPT expects a string, so we provide the JSON as a string.
        resume_content_json_string = resume_data.model_dump_json(indent=2)
        logger.info(
            f"Successfully converted input JSON data to string. Length: {len(resume_content_json_string)}"
        )

        latex_resume_text = await generate_latex_resume(
            resume_content=resume_content_json_string,  # Pass the JSON string here
            chain=latex_conversion_chain,
        )
        logger.info(
            f"Successfully generated LaTeX from JSON data. LaTeX length: {len(latex_resume_text)}"
        )

        pdf_content, pdf_filename = await convert_latex_to_pdf(latex_resume_text)
        logger.info(f"Successfully compiled LaTeX to PDF: {pdf_filename}")

        # Upload PDF to Supabase bucket and get public link
        # Ensure 'latex_output' directory exists (convert_latex_to_pdf should handle this, but good practice)
        latex_output_dir = os.path.join(os.getcwd(), "latex_output")
        os.makedirs(latex_output_dir, exist_ok=True)
        local_pdf_path = os.path.join(latex_output_dir, pdf_filename)

        # convert_latex_to_pdf already writes the file, so we just need to ensure the path is correct for upload
        if not os.path.exists(local_pdf_path):
            # This case should ideally not happen if convert_latex_to_pdf succeeds
            # and writes the file as expected.
            logger.error(
                f"PDF file not found at {local_pdf_path} after generation. This is unexpected."
            )
            # Fallback: attempt to write pdf_content to local_pdf_path if it wasn't found
            # This might indicate an issue in convert_latex_to_pdf's file handling logic if it occurs
            with open(local_pdf_path, "wb") as f_pdf:
                f_pdf.write(pdf_content)
            logger.info(
                f"Manually wrote PDF content to {local_pdf_path} as a fallback."
            )

        public_url = upload_pdf_to_bucket(local_pdf_path, pdf_filename)
        logger.info(f"Successfully uploaded PDF to Supabase. Public URL: {public_url}")

        # Insert record into resume_table
        insert_resume_record(public_url, user_id)  # Added source_type
        logger.info(
            f"Successfully inserted resume record for user {user_id} with URL {public_url}"
        )

        # Send email notification
        try:
            email_sent = await send_resume_conversion_notification(
                credentials=credentials,
                resume_link=public_url,
                conversion_type="json"
            )
            if email_sent:
                logger.info(f"Email notification sent to user {user_id}")
            else:
                logger.warning(f"Failed to send email notification to user {user_id}")
        except Exception as email_error:
            logger.error(f"Error sending email notification: {email_error}")
            # Don't fail the main request if email fails

        # Clean up generated files (PDF, .tex, .aux, .log, .out)
        base_name, _ = os.path.splitext(pdf_filename)
        extensions_to_clean = [".pdf", ".tex", ".aux", ".log", ".out"]
        for ext in extensions_to_clean:
            file_to_clean_path = os.path.join(latex_output_dir, f"{base_name}{ext}")
            try:
                if os.path.isfile(file_to_clean_path):
                    os.remove(file_to_clean_path)
                    logger.info(f"Cleaned up file: {file_to_clean_path}")
            except Exception as cleanup_err:
                logger.warning(f"Failed to delete {file_to_clean_path}: {cleanup_err}")

        end_time = time.time()
        processing_time_ms = (end_time - start_time) * 1000
        logger.info(
            f"Request /convert-json-to-latex completed in {processing_time_ms:.2f} ms for user {user_id}."
        )

        # Increment usage counters
        increment_user_usage(user_id, daily, monthly)
        daily_log_val = "N/A"
        if (
            hasattr(daily, "current_usage")
            and getattr(daily, "current_usage", None) is not None
        ):
            daily_log_val = str(daily.current_usage + 1)
        elif isinstance(daily, int):
            daily_log_val = str(daily + 1)

        monthly_log_val = "N/A"
        if (
            hasattr(monthly, "current_usage")
            and getattr(monthly, "current_usage", None) is not None
        ):
            monthly_log_val = str(monthly.current_usage + 1)
        elif isinstance(monthly, int):
            monthly_log_val = str(monthly + 1)
        logger.info(
            f"Incremented usage for user {user_id}. New usage: Daily={daily_log_val}, Monthly={monthly_log_val}"
        )

        return JsonToLatexResponse(resume_link=public_url, pdf_filename=pdf_filename)

    except HTTPException as he:
        logger.error(
            f"HTTPException in /convert-json-to-latex for user {user_id}: {he.detail}",
            exc_info=True,
        )
        raise he
    except ValueError as ve:  # For Pydantic validation errors or other value errors
        logger.error(
            f"ValueError in /convert-json-to-latex for user {user_id}: {str(ve)}",
            exc_info=True,
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except RuntimeError as re:
        logger.error(
            f"RuntimeError in /convert-json-to-latex for user {user_id}: {str(re)}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re)
        )
    except Exception as e:
        logger.error(
            f"Unexpected error in /convert-json-to-latex for user {user_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during JSON to LaTeX conversion.",
        )


if __name__ == "__main__":
    import uvicorn

    port = 8080  # Configure port here
    host = "127.0.0.1"  # Configure host here
    log_level = "info"  # Configure log level here

    logger.info(
        f"Starting Uvicorn server locally on {host}:{port} with log level {log_level}..."
    )
    uvicorn.run("main:app", host=host, port=port, log_level=log_level, reload=True)
