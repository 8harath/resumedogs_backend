# Resume Dogs Backend

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A production-grade FastAPI service that leverages artificial intelligence to provide intelligent resume tailoring and professional PDF generation using LaTeX. The system analyzes resume content against job descriptions, generates optimized versions, and produces publication-quality PDF documents.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Configuration](#environment-configuration)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Authentication & Authorization](#authentication--authorization)
- [Usage Examples](#usage-examples)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**Resume Dogs Backend** is an AI-powered service designed to help job seekers create tailored, professionally formatted resumes. The system addresses two critical challenges in modern job applications:

1. **Resume Tailoring**: Automatically adapting resume content to match specific job descriptions while maintaining authenticity and professional standards
2. **Professional Formatting**: Converting resume content into publication-quality LaTeX PDFs that meet industry formatting standards

The service is built with modern asynchronous Python, enterprise-grade authentication, and scalable cloud infrastructure.

### Use Cases

- **Job Seekers**: Quickly tailor resumes for multiple job applications
- **Career Services**: Provide automated resume optimization for students and alumni
- **Recruitment Platforms**: Integrate AI-powered resume enhancement into existing workflows
- **Research Projects**: Explore NLP applications in career development and document processing

---

## Key Features

### 1. AI-Powered Resume Tailoring
- Analyzes resume content against job descriptions using Google's Vertex AI
- Maintains factual accuracy while optimizing content presentation
- Supports multiple input formats (PDF, DOCX, Markdown, plain text)
- Preserves professional tone and formatting standards

### 2. Professional LaTeX PDF Generation
- Converts resumes to publication-quality LaTeX documents
- Automated compilation to PDF with error recovery
- Supports both file-based and structured JSON input
- Cloud storage integration with Supabase

### 3. Robust Authentication & Authorization
- JWT-based authentication with bearer token validation
- Usage tracking and rate limiting (daily/monthly quotas)
- Secure token verification using JWKS
- Support for anonymous and authenticated access modes

### 4. Enterprise-Ready Infrastructure
- Asynchronous request handling for high concurrency
- Docker containerization for consistent deployments
- CORS support for frontend integration
- Comprehensive logging and error handling
- Email notifications via Resend integration
- Optional Stripe webhook integration for payment processing

### 5. Multi-Format Support
- **Input**: PDF, DOCX, DOC, Markdown, TXT
- **Output**: LaTeX source, compiled PDF
- **API**: RESTful JSON with file upload support
- Hyperlink preservation from PDF sources

---

## Architecture

### System Design

```
┌─────────────────┐
│   Client Apps   │
│  (Web/Mobile)   │
└────────┬────────┘
         │
         │ HTTPS/Bearer Token
         ▼
┌─────────────────────────────────────────────────┐
│            FastAPI Application                   │
│  ┌──────────────────────────────────────────┐  │
│  │         Request Pipeline                  │  │
│  │  1. Authentication (JWT)                  │  │
│  │  2. Rate Limiting                         │  │
│  │  3. Input Validation (Pydantic)           │  │
│  │  4. File Processing                       │  │
│  └──────────────────────────────────────────┘  │
└────────┬───────────────┬────────────┬──────────┘
         │               │            │
         ▼               ▼            ▼
┌────────────────┐ ┌──────────┐ ┌──────────────┐
│  Google AI     │ │ Supabase │ │   Resend     │
│  Vertex AI     │ │ Database │ │   Email      │
│  (LangChain)   │ │ Storage  │ │   Service    │
└────────────────┘ └──────────┘ └──────────────┘
         │               │
         ▼               ▼
┌────────────────────────────┐
│     LaTeX Processing       │
│  • pdflatex compilation    │
│  • Template generation     │
│  • Error recovery          │
└────────────────────────────┘
         │
         ▼
┌────────────────────────────┐
│    PDF Storage & Delivery  │
│  • Supabase bucket upload  │
│  • Public URL generation   │
│  • Email notification      │
└────────────────────────────┘
```

### Request Flow

1. **Authentication Layer**: Validates JWT tokens and checks user quotas
2. **Processing Layer**: Extracts text from various file formats
3. **AI Layer**: Applies LangChain prompts to tailor content or generate LaTeX
4. **Compilation Layer**: Converts LaTeX to PDF using pdflatex
5. **Storage Layer**: Uploads PDFs to Supabase and generates public URLs
6. **Notification Layer**: Sends email confirmations with download links

---

## Technology Stack

### Core Framework
- **FastAPI** (0.115.12) - Modern, high-performance web framework with automatic OpenAPI documentation
- **Uvicorn** (0.34.0) - Lightning-fast ASGI server
- **Python** 3.11+ - Modern Python with type hints and async support

### AI & NLP
- **LangChain** (0.3.23) - LLM orchestration and prompt management
- **LangChain Google VertexAI** (2.0.25) - Google Cloud AI integration
- **langchain-google-genai** (2.1.2) - Google Generative AI models

### Document Processing
- **python-docx** (1.1.2) - Microsoft Word document parsing
- **PyMuPDF** (1.25.5) - Advanced PDF text extraction with hyperlink support
- **pypdf** (5.4.0) - PDF manipulation utilities
- **pdflatex** (0.1.3) - LaTeX to PDF compilation

### Database & Storage
- **Supabase** (2.15.0) - PostgreSQL database and object storage
- **SQLAlchemy** (2.0.40) - SQL toolkit and ORM

### Security & Authentication
- **PyJWT** (2.10.1) - JSON Web Token implementation
- **python-jose** - JWT cryptographic signing
- **passlib** - Password hashing utilities

### Communication & Integration
- **Resend** (2.15.0) - Transactional email service
- **Stripe** (12.0.0) - Payment processing webhooks
- **httpx** (0.28.1) - Modern HTTP client with async support

### Validation & Configuration
- **Pydantic** (2.11.2) - Data validation using Python type annotations
- **python-dotenv** (1.1.0) - Environment variable management
- **python-multipart** (0.0.20) - File upload handling

---

## Getting Started

### Prerequisites

#### Required Software
- **Python 3.11 or higher**
- **LaTeX Distribution**:
  - Linux: `sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-latex-extra`
  - macOS: Install [MacTeX](https://www.tug.org/mactex/)
  - Windows: Install [MiKTeX](https://miktex.org/)
- **Git** for version control

#### Required Services
- **Google Cloud Platform** account with Vertex AI API enabled
- **Supabase** project with:
  - PostgreSQL database
  - Storage bucket configured
  - Authentication enabled
- **Resend** account for email notifications (optional)
- **Stripe** account for payment processing (optional)

### Installation

#### Option 1: Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/resumedogs_backend.git
cd resumedogs_backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify LaTeX installation
pdflatex --version
```

#### Option 2: Docker Deployment

```bash
# Build the Docker image
docker build -t resumedogs-backend .

# Run the container
docker run -d \
  --name resumedogs \
  -p 8080:8080 \
  --env-file .env \
  resumedogs-backend
```

### Environment Configuration

Create a `.env` file in the project root with the following variables:

```env
# Google Cloud AI (Required)
GOOGLE_API_KEY=your_google_vertex_ai_api_key

# Supabase Configuration (Required)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_BUCKET=resumes
SUPABASE_JWKS_SECRET=your_jwt_secret_from_supabase

# Email Service (Optional - Required for notifications)
RESEND_API_KEY=your_resend_api_key

# Payment Processing (Optional)
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret

# Server Configuration (Optional)
PORT=8080
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

#### Environment Variable Details

| Variable | Purpose | Required | Example |
|----------|---------|----------|---------|
| `GOOGLE_API_KEY` | Google Vertex AI authentication | Yes | `AIza...` |
| `SUPABASE_URL` | Supabase project URL | Yes | `https://abc.supabase.co` |
| `SUPABASE_KEY` | Supabase anonymous key | Yes | `eyJ...` |
| `SUPABASE_BUCKET` | Storage bucket name | Yes | `resumes` |
| `SUPABASE_JWKS_SECRET` | JWT signing secret | Yes | `your-secret-key` |
| `RESEND_API_KEY` | Email service API key | No | `re_...` |
| `STRIPE_SECRET_KEY` | Stripe API key | No | `sk_test_...` |
| `STRIPE_WEBHOOK_SECRET` | Webhook verification | No | `whsec_...` |
| `PORT` | Server port | No | `8080` |
| `ALLOWED_ORIGINS` | CORS origins | No | `http://localhost:3000` |

### Running the Application

#### Development Mode
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8080
```

#### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
```

The API will be available at `http://localhost:8080`. Interactive API documentation is accessible at:
- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`

---

## API Documentation

### Base URL
```
http://localhost:8080  # Development
https://api.yourdomain.com  # Production
```

### Authentication
All protected endpoints require a JWT bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

### Endpoints

#### 1. Health Check

**Endpoint**: `GET /health`

**Description**: Verifies API availability and service status.

**Authentication**: Not required

**Response**:
```json
{
  "message": "API is running!"
}
```

**Status Codes**:
- `200 OK`: Service is operational

---

#### 2. Resume Tailoring

**Endpoint**: `POST /tailor`

**Description**: Analyzes a resume file and job description, returning an AI-optimized version tailored to the job requirements.

**Authentication**: Required (Bearer token)

**Request**:
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `resume_file` (file, required): Resume file in PDF, DOCX, MD, or TXT format (max 10MB)
  - `job_description` (string, required): Target job description (minimum 50 characters)

**Response**:
```json
{
  "filename": "john_doe_resume.pdf",
  "original_content_length": 1523,
  "job_description_length": 842,
  "tailored_resume_text": "JOHN DOE\nSoftware Engineer\n\nPROFESSIONAL SUMMARY\n..."
}
```

**Status Codes**:
- `200 OK`: Resume successfully tailored
- `400 Bad Request`: Invalid file format or job description too short
- `401 Unauthorized`: Missing or invalid authentication token
- `429 Too Many Requests`: Usage quota exceeded
- `500 Internal Server Error`: Processing error

**Example**:
```bash
curl -X POST "http://localhost:8080/tailor" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "resume_file=@resume.pdf" \
  -F "job_description=We are seeking a senior software engineer with 5+ years of experience in Python, FastAPI, and cloud technologies..."
```

---

#### 3. LaTeX PDF Generation (File Upload)

**Endpoint**: `POST /convert-latex`

**Description**: Converts a resume file to a professionally formatted LaTeX PDF.

**Authentication**: Required (Bearer token)

**Request**:
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `resume_file` (file, required): Resume file in PDF, DOCX, DOC, or MD format (max 10MB)

**Response**:
```json
{
  "message": "Resume converted successfully.",
  "resume_link": "https://your-project.supabase.co/storage/v1/object/public/resumes/abc123.pdf",
  "pdf_filename": "resume_abc123.pdf"
}
```

**Additional Actions**:
- Uploads PDF to Supabase storage
- Sends email notification with download link
- Records conversion in database

**Status Codes**:
- `200 OK`: PDF successfully generated
- `400 Bad Request`: Invalid file format or upload error
- `401 Unauthorized`: Missing or invalid authentication token
- `429 Too Many Requests`: Usage quota exceeded
- `500 Internal Server Error`: Compilation or upload error

**Example**:
```bash
curl -X POST "http://localhost:8080/convert-latex" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "resume_file=@resume.docx"
```

---

#### 4. LaTeX PDF Generation (JSON Input)

**Endpoint**: `POST /convert-json-to-latex`

**Description**: Generates a LaTeX PDF from structured resume data in JSON format.

**Authentication**: Required (Bearer token)

**Request**:
- **Content-Type**: `application/json`
- **Body**: ResumeData JSON object

**Request Schema**:
```json
{
  "basicInfo": {
    "fullName": "John Doe",
    "phone": "+1-555-123-4567",
    "email": "john.doe@example.com",
    "linkedin": "linkedin.com/in/johndoe",
    "github": "github.com/johndoe",
    "website": "johndoe.dev"
  },
  "education": [
    {
      "id": "edu1",
      "institution": "University of Example",
      "location": "City, State",
      "degree": "Bachelor of Science in Computer Science",
      "minor": "Mathematics",
      "startDate": "2016-09",
      "endDate": "2020-05",
      "isPresent": false
    }
  ],
  "experience": [
    {
      "id": "exp1",
      "organization": "Tech Company Inc.",
      "jobTitle": "Senior Software Engineer",
      "location": "San Francisco, CA",
      "startDate": "2020-06",
      "endDate": null,
      "isPresent": true,
      "description": [
        "Led development of microservices architecture serving 1M+ users",
        "Reduced API response time by 40% through optimization",
        "Mentored team of 5 junior engineers"
      ]
    }
  ],
  "projects": [
    {
      "id": "proj1",
      "name": "Open Source ML Framework",
      "technologies": "Python, TensorFlow, Docker",
      "startDate": "2021-01",
      "endDate": "2021-12",
      "isPresent": false,
      "description": [
        "Developed ML framework with 500+ GitHub stars",
        "Implemented CI/CD pipeline reducing deployment time by 60%"
      ]
    }
  ],
  "skills": {
    "languages": "Python, JavaScript, TypeScript, Java",
    "frameworks": "FastAPI, React, Node.js, Spring Boot",
    "developerTools": "Git, Docker, Kubernetes, AWS",
    "libraries": "TensorFlow, PyTorch, Pandas, NumPy"
  }
}
```

**Response**:
```json
{
  "message": "Resume converted successfully from JSON.",
  "resume_link": "https://your-project.supabase.co/storage/v1/object/public/resumes/def456.pdf",
  "pdf_filename": "resume_def456.pdf"
}
```

**Status Codes**:
- `200 OK`: PDF successfully generated
- `400 Bad Request`: Invalid JSON schema
- `401 Unauthorized`: Missing or invalid authentication token
- `429 Too Many Requests`: Usage quota exceeded
- `500 Internal Server Error`: Compilation or upload error

**Example**:
```bash
curl -X POST "http://localhost:8080/convert-json-to-latex" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d @resume_data.json
```

---

#### 5. Stripe Webhook Handler

**Endpoint**: `POST /webhook/stripe`

**Description**: Receives and processes Stripe webhook events for payment processing.

**Authentication**: Stripe signature verification

**Request**:
- **Content-Type**: `application/json`
- **Headers**: `Stripe-Signature` header for verification
- **Body**: Raw Stripe webhook payload

**Supported Events**:
- `checkout.session.completed`: Handles successful payment completions

**Response**:
```json
{
  "message": "Webhook received and processed"
}
```

**Status Codes**:
- `200 OK`: Webhook successfully processed
- `400 Bad Request`: Invalid signature or payload
- `503 Service Unavailable`: Stripe not configured

**Note**: This endpoint should only be accessible by Stripe's webhook servers. Configure webhook URL in Stripe Dashboard.

---

### Rate Limiting

All authenticated endpoints enforce the following usage quotas:

| Quota Type | Limit | Reset Period |
|------------|-------|--------------|
| Daily conversions | 3 | 24 hours |
| Monthly conversions | 30 | 30 days |

When quota is exceeded, the API returns:
```json
{
  "detail": "Daily conversion limit reached. Please try again tomorrow."
}
```

**Status Code**: `429 Too Many Requests`

---

## Project Structure

```
resumedogs_backend/
├── main.py                      # FastAPI application entry point, route definitions
├── models.py                    # Pydantic models for request/response validation
├── requirements.txt             # Python package dependencies
├── Dockerfile                   # Docker container configuration
├── .dockerignore                # Docker build exclusions
├── .gitignore                   # Git tracking exclusions
│
├── README.md                    # This comprehensive documentation
├── EMAIL_SETUP.md               # Email integration guide
├── Enhancements.md              # Proposed improvements and extensions
│
├── resume_processor.py          # AI-powered resume tailoring logic
├── latex_converter.py           # LaTeX compilation and PDF generation
├── latex_utils.py               # LaTeX utility functions (file I/O, pdflatex)
├── utils.py                     # File extraction (PDF, DOCX, MD, TXT)
│
├── auth.py                      # Bearer token authentication scheme
├── auth_utils.py                # JWT token parsing and validation
├── usage.py                     # Usage tracking and quota enforcement
│
├── supabase_utils.py            # Supabase database and storage integration
├── email_service.py             # Resend email service integration
├── email_templates.py           # HTML email templates
├── payments.py                  # Stripe webhook processing
│
├── prompts.py                   # AI prompt templates (configurable)
└── increase_user_usage.py       # Usage increment utility
```

### Core Modules

#### Application Layer
- **`main.py`**: FastAPI application initialization, CORS configuration, route registration, middleware setup

#### Processing Layer
- **`resume_processor.py`**: LangChain integration, AI tailoring logic, prompt application
- **`latex_converter.py`**: LaTeX document generation, pdflatex compilation, error recovery
- **`latex_utils.py`**: File operations, pdflatex command execution, temporary file management
- **`utils.py`**: Multi-format file reading (PDF with hyperlinks, DOCX, DOC, Markdown, TXT)

#### Security Layer
- **`auth.py`**: FastAPI security dependency, bearer token extraction
- **`auth_utils.py`**: JWT decoding, user extraction, token validation
- **`usage.py`**: Daily/monthly quota checking, usage increment

#### Integration Layer
- **`supabase_utils.py`**: PDF upload to storage bucket, database record insertion
- **`email_service.py`**: Email sending via Resend API
- **`email_templates.py`**: Professional HTML email templates with responsive design
- **`payments.py`**: Stripe event handling, signature verification

#### Configuration Layer
- **`models.py`**: Type-safe data models, request/response schemas
- **`prompts.py`**: Customizable AI prompts for tailoring and LaTeX generation

---

## Authentication & Authorization

### JWT Token Structure

The system expects JWT tokens with the following claims:

```json
{
  "sub": "user_uuid_123",
  "email": "user@example.com",
  "iat": 1234567890,
  "exp": 1234571490
}
```

**Required Claims**:
- `sub`: Unique user identifier (used for quota tracking)
- `email`: User email address (used for notifications)

### Token Validation

1. **Signature Verification**: Validates JWT signature using `SUPABASE_JWKS_SECRET`
2. **Expiration Check**: Ensures token is not expired
3. **User Extraction**: Extracts user_id and email from claims
4. **Quota Verification**: Checks daily and monthly usage limits

### Usage Tracking

User conversions are tracked in the `user_usage` table:

```sql
CREATE TABLE user_usage (
  user_id TEXT PRIMARY KEY,
  daily_conversions INTEGER DEFAULT 0,
  monthly_conversions INTEGER DEFAULT 0,
  last_daily_reset TIMESTAMP,
  last_monthly_reset TIMESTAMP
);
```

**Daily Limit**: 3 conversions (resets every 24 hours)
**Monthly Limit**: 30 conversions (resets every 30 days)

### Anonymous Access Configuration

For testing or development, you can configure anonymous access by modifying the `User` model default credits:

```python
# models.py
class User(BaseModel):
    user_id: str
    email: str | None = None
    credits: int = 999  # High default for anonymous access
```

---

## Usage Examples

### Python Client

```python
import requests
import json

BASE_URL = "http://localhost:8080"
JWT_TOKEN = "your_jwt_token_here"

headers = {
    "Authorization": f"Bearer {JWT_TOKEN}"
}

# Example 1: Tailor a resume
with open("resume.pdf", "rb") as resume_file:
    files = {"resume_file": resume_file}
    data = {
        "job_description": "We are seeking a senior Python developer with experience in FastAPI, "
                          "Docker, and cloud technologies. The ideal candidate will have 5+ years "
                          "of backend development experience and strong knowledge of RESTful APIs."
    }

    response = requests.post(
        f"{BASE_URL}/tailor",
        headers=headers,
        files=files,
        data=data
    )

    if response.status_code == 200:
        result = response.json()
        print(f"Tailored resume:\n{result['tailored_resume_text']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Example 2: Convert resume to LaTeX PDF
with open("resume.docx", "rb") as resume_file:
    files = {"resume_file": resume_file}

    response = requests.post(
        f"{BASE_URL}/convert-latex",
        headers=headers,
        files=files
    )

    if response.status_code == 200:
        result = response.json()
        print(f"PDF available at: {result['resume_link']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Example 3: Generate PDF from JSON
resume_data = {
    "basicInfo": {
        "fullName": "Jane Smith",
        "phone": "+1-555-987-6543",
        "email": "jane.smith@example.com",
        "linkedin": "linkedin.com/in/janesmith",
        "github": "github.com/janesmith",
        "website": "janesmith.dev"
    },
    "education": [{
        "id": "edu1",
        "institution": "Stanford University",
        "location": "Stanford, CA",
        "degree": "Master of Science in Computer Science",
        "minor": None,
        "startDate": "2018-09",
        "endDate": "2020-06",
        "isPresent": False
    }],
    "experience": [{
        "id": "exp1",
        "organization": "Google",
        "jobTitle": "Software Engineer",
        "location": "Mountain View, CA",
        "startDate": "2020-07",
        "endDate": None,
        "isPresent": True,
        "description": [
            "Developed scalable backend services using Go and Python",
            "Improved system performance by 35% through optimization"
        ]
    }],
    "projects": [],
    "skills": {
        "languages": "Python, Go, JavaScript",
        "frameworks": "FastAPI, Flask, React",
        "developerTools": "Git, Docker, Kubernetes, GCP",
        "libraries": "NumPy, Pandas, TensorFlow"
    }
}

response = requests.post(
    f"{BASE_URL}/convert-json-to-latex",
    headers=headers,
    json=resume_data
)

if response.status_code == 200:
    result = response.json()
    print(f"PDF generated: {result['resume_link']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

### JavaScript/TypeScript Client

```typescript
const BASE_URL = "http://localhost:8080";
const JWT_TOKEN = "your_jwt_token_here";

// Example 1: Tailor resume
async function tailorResume(resumeFile: File, jobDescription: string) {
  const formData = new FormData();
  formData.append("resume_file", resumeFile);
  formData.append("job_description", jobDescription);

  const response = await fetch(`${BASE_URL}/tailor`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${JWT_TOKEN}`
    },
    body: formData
  });

  if (response.ok) {
    const data = await response.json();
    console.log("Tailored resume:", data.tailored_resume_text);
    return data;
  } else {
    throw new Error(`Error: ${response.status} - ${await response.text()}`);
  }
}

// Example 2: Convert to LaTeX PDF
async function convertToLatex(resumeFile: File) {
  const formData = new FormData();
  formData.append("resume_file", resumeFile);

  const response = await fetch(`${BASE_URL}/convert-latex`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${JWT_TOKEN}`
    },
    body: formData
  });

  if (response.ok) {
    const data = await response.json();
    console.log("PDF URL:", data.resume_link);
    return data;
  } else {
    throw new Error(`Error: ${response.status} - ${await response.text()}`);
  }
}

// Example 3: Generate from JSON
async function generateFromJSON(resumeData: any) {
  const response = await fetch(`${BASE_URL}/convert-json-to-latex`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${JWT_TOKEN}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(resumeData)
  });

  if (response.ok) {
    const data = await response.json();
    console.log("Generated PDF:", data.resume_link);
    return data;
  } else {
    throw new Error(`Error: ${response.status} - ${await response.text()}`);
  }
}
```

### cURL Examples

```bash
# Health check
curl -X GET "http://localhost:8080/health"

# Tailor resume
curl -X POST "http://localhost:8080/tailor" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "resume_file=@/path/to/resume.pdf" \
  -F "job_description=Your detailed job description here (minimum 50 characters)..."

# Convert to LaTeX PDF
curl -X POST "http://localhost:8080/convert-latex" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "resume_file=@/path/to/resume.docx"

# Generate from JSON
curl -X POST "http://localhost:8080/convert-json-to-latex" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "basicInfo": {
      "fullName": "John Doe",
      "phone": "+1-555-0123",
      "email": "john@example.com",
      "linkedin": "linkedin.com/in/johndoe",
      "github": "github.com/johndoe"
    },
    "education": [],
    "experience": [],
    "projects": [],
    "skills": {
      "languages": "Python, JavaScript",
      "frameworks": "FastAPI, React",
      "developerTools": "Git, Docker",
      "libraries": "NumPy, Pandas"
    }
  }'
```

---

## Deployment

### Docker Production Deployment

```bash
# Build production image
docker build -t resumedogs-backend:latest .

# Run with environment file
docker run -d \
  --name resumedogs-prod \
  -p 8080:8080 \
  --env-file .env.production \
  --restart unless-stopped \
  resumedogs-backend:latest

# View logs
docker logs -f resumedogs-prod

# Stop container
docker stop resumedogs-prod
```

### Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    container_name: resumedogs-api
    ports:
      - "8080:8080"
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
    environment:
      - PORT=8080
      - WORKERS=4
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Cloud Platform Deployment

#### Google Cloud Run

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/your-project-id/resumedogs-backend

# Deploy to Cloud Run
gcloud run deploy resumedogs-backend \
  --image gcr.io/your-project-id/resumedogs-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY,SUPABASE_URL=$SUPABASE_URL
```

#### AWS Elastic Container Service

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account-id.dkr.ecr.us-east-1.amazonaws.com
docker tag resumedogs-backend:latest your-account-id.dkr.ecr.us-east-1.amazonaws.com/resumedogs-backend:latest
docker push your-account-id.dkr.ecr.us-east-1.amazonaws.com/resumedogs-backend:latest

# Create ECS task definition and service (use AWS Console or CLI)
```

#### Heroku

```bash
# Login to Heroku
heroku login
heroku container:login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set GOOGLE_API_KEY=your_key
heroku config:set SUPABASE_URL=your_url

# Deploy
heroku container:push web
heroku container:release web
```

### Production Checklist

- [ ] Configure production environment variables
- [ ] Set up SSL/TLS certificates
- [ ] Configure CORS for production domains
- [ ] Set up monitoring and logging (Sentry, Datadog, etc.)
- [ ] Configure database backups
- [ ] Set up CI/CD pipeline
- [ ] Enable rate limiting at infrastructure level
- [ ] Configure health checks and auto-scaling
- [ ] Set up error alerting
- [ ] Review security settings (JWT secret rotation, API keys)
- [ ] Test email delivery in production
- [ ] Configure Stripe webhooks for production
- [ ] Document API versioning strategy

---

## Troubleshooting

### Common Issues

#### 1. LaTeX Compilation Errors

**Symptom**: PDF generation fails with pdflatex errors

**Solutions**:
```bash
# Verify LaTeX installation
pdflatex --version

# Install missing LaTeX packages (Linux)
sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-latex-extra

# Check for special characters in resume content
# LaTeX special characters: # $ % ^ & _ { } ~ \
```

**Note**: The system includes error recovery logic that tolerates pdflatex warnings if a PDF is successfully generated.

#### 2. JWT Authentication Failures

**Symptom**: 401 Unauthorized errors despite valid token

**Solutions**:
```python
# Verify JWT secret configuration
# Check that SUPABASE_JWKS_SECRET matches your Supabase project

# Decode token to inspect claims
import jwt
token = "your_token_here"
decoded = jwt.decode(token, options={"verify_signature": False})
print(decoded)  # Check for 'sub' and 'email' fields

# Ensure token is not expired
from datetime import datetime
exp_timestamp = decoded.get('exp', 0)
print(f"Token expires: {datetime.fromtimestamp(exp_timestamp)}")
```

#### 3. File Upload Issues

**Symptom**: 400 Bad Request on file upload

**Solutions**:
- Verify file size is under 10MB
- Check file extension matches supported formats (PDF, DOCX, DOC, MD, TXT)
- Ensure Content-Type header is `multipart/form-data`
- Verify file is not corrupted

```bash
# Test file validity
file resume.pdf  # Should show: PDF document
head -c 10 resume.pdf  # Should start with %PDF
```

#### 4. Supabase Connection Errors

**Symptom**: 500 errors with "Could not upload PDF to Supabase"

**Solutions**:
```python
# Test Supabase connection
from supabase import create_client
import os

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Check bucket exists
buckets = supabase.storage.list_buckets()
print([b.name for b in buckets])

# Verify bucket permissions (should be public for PDF downloads)
```

#### 5. Email Delivery Failures

**Symptom**: PDFs generate but emails not received

**Solutions**:
- Verify `RESEND_API_KEY` is set in environment
- Check email service logs for errors
- Confirm sender domain is verified in Resend dashboard
- Verify JWT token contains `email` field

```bash
# Test email configuration
curl https://api.resend.com/emails \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "onboarding@resend.dev",
    "to": "your@email.com",
    "subject": "Test",
    "html": "<p>Test email</p>"
  }'
```

#### 6. Rate Limit Exceeded

**Symptom**: 429 Too Many Requests error

**Solutions**:
- Check current usage in `user_usage` table
- Wait for quota reset (24 hours for daily, 30 days for monthly)
- Increase limits in `usage.py` if needed (for development)

```python
# Check user usage (requires database access)
from supabase_utils import supabase
usage = supabase.table('user_usage').select('*').eq('user_id', 'user_id_here').execute()
print(usage.data)
```

#### 7. AI Processing Errors

**Symptom**: Resume tailoring returns generic or incomplete content

**Solutions**:
- Verify `GOOGLE_API_KEY` is valid and has quota available
- Check prompts in `prompts.py` are configured correctly
- Ensure job description is substantive (minimum 50 characters)
- Review LangChain logs for API errors

```python
# Test Google AI connection
from langchain_google_genai import ChatGoogleGenerativeAI
import os

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

response = llm.invoke("Hello, this is a test")
print(response)
```

### Debug Mode

Enable detailed logging:

```python
# Add to main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check logs for detailed error traces:
```bash
# Docker logs
docker logs -f resumedogs-prod

# Local logs
tail -f logs/app.log  # If logging to file
```

### Performance Optimization

If experiencing slow response times:

1. **Enable caching** for repeated requests
2. **Increase Uvicorn workers**: `--workers 8`
3. **Use async I/O** for all external calls
4. **Monitor LaTeX compilation time** (typically 2-5 seconds)
5. **Optimize AI prompt length** to reduce token usage
6. **Consider Redis** for session/quota caching

---

## Security Considerations

### Current Security Measures

1. **Authentication**:
   - JWT bearer token validation
   - Token signature verification using JWKS
   - Expiration checking

2. **Authorization**:
   - Per-user usage quotas (daily/monthly)
   - Rate limiting enforcement

3. **Input Validation**:
   - Pydantic model validation for all requests
   - File size limits (10MB max)
   - File type restrictions
   - Minimum job description length (50 characters)

4. **External Service Security**:
   - Stripe webhook signature verification
   - HTTPS for all external API calls
   - Environment variable for sensitive credentials

5. **Error Handling**:
   - No sensitive information in error responses
   - Comprehensive logging for security monitoring
   - Graceful degradation on service failures

### Security Recommendations

#### Production Hardening

1. **CORS Configuration**:
```python
# In main.py - Replace wildcard with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://app.yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
```

2. **API Rate Limiting** (Infrastructure Level):
```nginx
# Nginx rate limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req zone=api_limit burst=20 nodelay;
```

3. **Input Sanitization**:
   - Validate all file uploads for malicious content
   - Scan PDFs for embedded scripts
   - Sanitize LaTeX input to prevent command injection

4. **Secrets Management**:
   - Use cloud secret managers (AWS Secrets Manager, GCP Secret Manager)
   - Rotate JWT secrets regularly
   - Never commit `.env` files to version control

5. **Monitoring & Alerting**:
   - Set up intrusion detection
   - Monitor for unusual API patterns
   - Alert on repeated authentication failures
   - Track quota abuse patterns

#### OWASP Top 10 Compliance

- **A01: Broken Access Control**: Implemented via JWT validation and usage quotas
- **A02: Cryptographic Failures**: Using industry-standard JWT signing
- **A03: Injection**: Pydantic validation prevents SQL injection; LaTeX sanitization needed
- **A04: Insecure Design**: Rate limiting and authentication in place
- **A05: Security Misconfiguration**: Review CORS and error message verbosity
- **A07: Identification and Authentication Failures**: JWT token validation implemented
- **A08: Software and Data Integrity Failures**: Dependency pinning in requirements.txt

### Known Limitations

1. **CORS**: Currently allows all origins (`["*"]`) - should be restricted in production
2. **Prompt Injection**: AI prompts could be manipulated through malicious job descriptions
3. **Resource Exhaustion**: Large file uploads or complex LaTeX could cause timeouts
4. **Prompt Templates**: Empty prompts in `prompts.py` need configuration
5. **No Request ID Tracking**: Difficult to trace individual requests across logs

---

## Contributing

We welcome contributions to improve Resume Dogs Backend! Here's how you can help:

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** with clear, documented code
4. **Add tests** for new functionality
5. **Run the test suite**:
   ```bash
   pytest tests/
   ```
6. **Commit with clear messages**:
   ```bash
   git commit -m "Add: Feature description"
   ```
7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Submit a Pull Request** with detailed description

### Code Standards

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for all function signatures
- Write docstrings for all public functions
- Keep functions focused and under 50 lines when possible
- Use meaningful variable names

### Testing Guidelines

```python
# Example test structure
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running!"}

def test_tailor_without_auth():
    response = client.post("/tailor")
    assert response.status_code == 401
```

### Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add examples for new features
- Update Enhancements.md if proposing new features

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Resume Dogs Backend

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Acknowledgments

- **FastAPI** for the excellent modern Python web framework
- **LangChain** for streamlined LLM integration
- **Google Vertex AI** for powerful generative AI capabilities
- **Supabase** for robust backend-as-a-service infrastructure
- **Resend** for reliable transactional email delivery

---

## Support & Contact

- **Documentation**: [GitHub Wiki](https://github.com/yourusername/resumedogs_backend/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/resumedogs_backend/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/resumedogs_backend/discussions)

---

## Changelog

### Version 0.2.0 (Current)
- Initial public release
- Core resume tailoring functionality
- LaTeX PDF generation from files and JSON
- JWT authentication and usage quotas
- Email notification system
- Stripe webhook integration
- Docker containerization

---

**Built with ❤️ for job seekers everywhere**
