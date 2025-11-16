# Resume Tailoring API

## Overview

This FastAPI backend server provides an API for tailoring resumes based on job descriptions and converting resumes into professionally formatted LaTeX PDFs. It includes basic authentication capabilities and optional payment processing via Stripe webhooks.

## Key Features

- **Resume Tailoring:** Processes resumes to match job descriptions while maintaining truthfulness and professional formatting [cite: cv_bandar/resume_processor.py].

- **LaTeX PDF Generation:** Converts tailored resumes into professionally formatted LaTeX documents and compiles them into PDFs [cite: cv_bandar/latex_converter.py].

- **Authentication:** Includes a simple Bearer token authentication system that can be configured for anonymous access or extended for full authentication [cite: cv_bandar/auth.py, cv_bandar/main.py].

- **Credit System:** Basic credit tracking system that can be used to limit API usage [cite: cv_bandar/auth.py, cv_bandar/main.py].

- **Payment Processing:** Optional Stripe webhook integration for handling payments [cite: cv_bandar/payments.py, cv_bandar/main.py].

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone <repository-url>
   cd cv_bandar
   ```

2. **Create and Activate Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install fastapi uvicorn python-dotenv langchain-google-genai langchain-core python-docx pypdf httpx[http2] stripe python-multipart python-jose[cryptography] passlib[bcrypt] pdflatex # Add any other missing dependencies
   ```

4. **Environment Variables:**
   Create a `.env` file in the project root with:

   ```
   # Configure environment variables as needed
   # GOOGLE_API_KEY=<Your_Google_AI_API_Key>
   # STRIPE_SECRET_KEY=<Your_Stripe_Secret_Key>  # Optional
   # STRIPE_WEBHOOK_SECRET=<Your_Stripe_Webhook_Secret>  # Optional
   # ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
   ```

5. **LaTeX Setup:**

   - Install a LaTeX distribution (e.g., TexLive) if you plan to use PDF generation.
   - Ensure the `pdflatex` command is available in your system PATH.

6. **Run the Server:**
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation

### Endpoints

#### POST /tailor

- **Description:** Receives a resume file and job description, and returns a tailored version of the resume.
- **Authentication:** Requires Bearer token (or configured for anonymous access).
- **Request:**
  - `resume_file`: File (PDF, DOCX, or TXT)
  - `job_description`: String (minimum 50 characters)
- **Response:** JSON containing the tailored resume text and metadata.
- **Status Codes:**
  - `200 OK`: Success
  - `400 Bad Request`: Invalid input
  - `401 Unauthorized`: Missing or invalid authentication
  - `500 Internal Server Error`: Processing error

#### POST /convert-latex

- **Description:** Converts a resume to LaTeX format and returns a compiled PDF.
- **Authentication:** Requires Bearer token (or configured for anonymous access).
- **Request:**
  - `resume_file`: File (PDF or MD)
- **Response:** PDF file
- **Status Codes:**
  - `200 OK`: Success
  - `400 Bad Request`: Invalid input
  - `401 Unauthorized`: Missing or invalid authentication
  - `500 Internal Server Error`: Processing error

#### POST /webhook/stripe

- **Description:** Receives webhook events from Stripe. It verifies the Stripe signature and processes relevant events (currently `checkout.session.completed`). This endpoint should only be accessible by Stripe.
- **Authentication:** Requires valid Stripe signature
- **Request:** Raw webhook payload from Stripe
- **Response:** Confirmation message
- **Status Codes:**
  - `200 OK`: Success
  - `400 Bad Request`: Invalid signature or payload
  - `503 Service Unavailable`: If Stripe keys are not configured [cite: cv_bandar/payments.py].

## Project Structure

- **`main.py`**: Application entry point. Sets up FastAPI app, defines routes, and configures middleware [cite: cv_bandar/main.py].

- **`resume_processor.py`**: Core logic for resume tailoring and processing [cite: cv_bandar/resume_processor.py].

- **`latex_converter.py`**: Handles conversion of resume text to LaTeX format and PDF compilation [cite: cv_bandar/latex_converter.py].

- **`auth.py`**: Implements basic authentication logic. Includes the `get_current_user` dependency to protect endpoints and check credits, and the `decrement_user_credits` function [cite: cv_bandar/auth.py].

- **`payments.py`**: Handles Stripe webhook processing for payment integration [cite: cv_bandar/payments.py].

- **`models.py`**: Pydantic models for request/response validation [cite: cv_bandar/models.py].

- **`utils.py`**: Utility functions for file handling and text extraction [cite: cv_bandar/utils.py].

- **`prompts.py`**: Contains prompt template placeholders for resume tailoring and LaTeX conversion [cite: cv_bandar/prompts.py].

## Error Handling

- Comprehensive error handling throughout the application
- Detailed logging for debugging and monitoring
- Graceful fallbacks for missing configurations
- Input validation using Pydantic models

## Security Considerations

- Bearer token authentication
- CORS configuration for frontend integration
- Stripe webhook signature verification
- Credit limit enforcement
- Input validation and sanitization

## Contributing

Please submit issues and pull requests for any improvements or bug fixes.

## License

[Your chosen license]
