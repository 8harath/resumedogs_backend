# /backend/models.py
from pydantic import BaseModel, Field

class TailoredResumeResponse(BaseModel):
    """Response model for the /tailor endpoint."""
    filename: str = Field(..., description="Original filename of the uploaded resume.")
    original_content_length: int = Field(..., description="Number of characters extracted from the original resume.")
    job_description_length: int = Field(..., description="Number of characters in the provided job description.")
    tailored_resume_text: str = Field(..., description="The tailored resume content.")

class User(BaseModel):
    """Simple user model for anonymous access."""
    user_id: str
    email: str | None = None
    credits: int = 999  # Set high default for anonymous access

class MessageResponse(BaseModel):
    """Generic message response model."""
    message: str

class BasicInfo(BaseModel):
    fullName: str
    phone: str
    email: str
    linkedin: str
    github: str
    website: str | None = None # Optional field

class EducationItem(BaseModel):
    id: str
    institution: str
    location: str
    degree: str
    minor: str | None = None # Optional field
    startDate: str # Keep as string, assume ISO date format as per user
    endDate: str | None = None # Keep as string or null
    isPresent: bool

class ExperienceItem(BaseModel):
    id: str
    organization: str
    jobTitle: str
    location: str
    startDate: str # Keep as string
    endDate: str | None = None # Keep as string or null
    isPresent: bool
    description: list[str]

class ProjectItem(BaseModel):
    id: str
    name: str
    technologies: str
    startDate: str # Keep as string
    endDate: str | None = None # Keep as string or null
    isPresent: bool
    description: list[str]

class Skills(BaseModel):
    languages: str
    frameworks: str
    developerTools: str
    libraries: str

class ResumeData(BaseModel):
    basicInfo: BasicInfo
    education: list[EducationItem]
    experience: list[ExperienceItem]
    projects: list[ProjectItem]
    skills: Skills

class JsonToLatexResponse(BaseModel):
    message: str = Field(default="Resume converted successfully from JSON.")
    resume_link: str | None = None
    pdf_filename: str | None = None