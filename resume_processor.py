# /backend/resume_processor.py
import os
import logging
import datetime

# LangChain imports
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from langchain_core.exceptions import OutputParserException

# Custom prompt imports
from prompts import RESUME_TAILORING_PROMPT, LATEX_CONVERSION_PROMPT, LATEX_TEMPLATE

logger = logging.getLogger(__name__)

# --- LangChain Setup Function ---


def setup_resume_tailoring_chain(
    model_name: str = None,  # Set model name here
    temperature: float = 0.7,
) -> tuple[RunnableSequence, RunnableSequence]:
    """
    Initializes the model, loads prompts, sets up
    parsers, and returns both the resume tailoring and LaTeX conversion chains.
    """
    # 1. Load API Key (should be loaded already by main app)
    # google_api_key = os.getenv("GOOGLE_API_KEY")

    # if not google_api_key:
    #     logger.error("GOOGLE_API_KEY is not available in environment variables.")
    #     raise ValueError("GOOGLE_API_KEY is not configured.")

    # # 2. Initialize the model
    try:
        logger.info(f"Initializing model: {model_name}...")
        llm = ChatVertexAI(
            model_name=model_name,
            project=None,  # Set Google Cloud project here
            location=None,  # Set Google Cloud location here
            temperature=temperature,
        )
        logger.info("Model initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing model: {e}", exc_info=True)
        raise RuntimeError(f"Could not initialize model: {e}")

    # 4. Create Prompt Templates
    resume_prompt = ChatPromptTemplate.from_template(RESUME_TAILORING_PROMPT)
    latex_prompt = ChatPromptTemplate.from_template(LATEX_CONVERSION_PROMPT)

    # 5. Define Output Parser
    output_parser = StrOutputParser()

    # 6. Create and return both LangChain Chains
    logger.info("Creating processing chains...")
    resume_chain = resume_prompt | llm | output_parser
    latex_chain = latex_prompt | llm | output_parser
    logger.info("LangChain chains created.")
    return resume_chain, latex_chain


# --- Core Tailoring Function ---
async def generate_tailored_resume(
    resume_content: str, job_description: str, chain: RunnableSequence
) -> str:
    """
    Takes original resume text, job description text, and a pre-configured
    LangChain chain, and returns a tailored resume string (asynchronously).
    """
        logger.info("Processing resume tailoring...")
    if not resume_content or not job_description:
        logger.error("Attempted to tailor resume with empty content.")
        raise ValueError("Resume content and job description cannot be empty.")

    try:
        # Use chain.ainvoke for async operation within FastAPI
        tailored_resume = await chain.ainvoke(
            {"resume_content": resume_content, "job_description": job_description}
        )
        logger.info(
            f"Processing successful (Output length: {len(tailored_resume)})."
        )

        if not isinstance(tailored_resume, str) or not tailored_resume.strip():
            logger.error("Processing returned empty or non-string output.")
            raise RuntimeError("Failed to generate valid resume text.")

        if len(tailored_resume) < 100:  # Arbitrary short length check
            logger.warning(
                f"Output seems very short ({len(tailored_resume)} chars). Possible error."
            )
            # Example check for refusal patterns
            refusal_patterns = [
                "provide the content",
                "ready to help",
                "cannot fulfill",
                "i need the resume",
            ]
            if any(p in tailored_resume.lower() for p in refusal_patterns):
                logger.error(
                    "Response indicates it didn't process the input correctly."
                )
                raise RuntimeError(
                    "Failed to process the input resume/JD. Please check the input data."
                )

        return tailored_resume.strip()  # Return stripped text

    except OutputParserException as ope:
        logger.error(f"An error occurred parsing the output: {ope}", exc_info=True)
        raise RuntimeError(f"Failed to parse output: {ope}")
    except Exception as e:
        # Catch specific API errors if possible (e.g., RateLimitError, AuthenticationError)
        logger.error(
            f"An error occurred during LangChain chain invocation: {e}", exc_info=True
        )
        raise RuntimeError(f"Processing failed: {e}")


# --- LaTeX Conversion Function ---
async def generate_latex_resume(resume_content: str, chain: RunnableSequence) -> str:
    """
    Takes original resume text and converts it to LaTeX format using the provided chain.
    Returns a string containing valid LaTeX code for a professional resume.
    """
    if not resume_content:
        logger.error("Attempted to convert empty resume content")
        raise ValueError("Resume content cannot be empty")

    # Define base_dir to save the .tex file
    base_dir = os.getcwd()  # Configure output directory here

    try:
        # Use the template from prompts.py instead of reading from file
        latex_resume = await chain.ainvoke(
            {"resume_content": resume_content, "latex_template": LATEX_TEMPLATE}
        )

        # Basic validation
        if not isinstance(latex_resume, str):
            raise RuntimeError("Model output is not a string")

        # Only remove markdown code block markers, preserve all LaTeX content
        if latex_resume.startswith("```latex\n"):
            latex_resume = latex_resume[8:]  # Remove ```latex\n prefix
        if latex_resume.endswith("\n```"):
            latex_resume = latex_resume[:-4]  # Remove ```\n suffix

        return latex_resume

    except Exception as e:
        logger.error(f"Error during LaTeX conversion: {e}", exc_info=True)
        raise RuntimeError(f"LaTeX conversion failed: {e}")
