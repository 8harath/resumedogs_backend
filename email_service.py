"""
Email service for sending resume conversion notifications using Resend.
"""
import logging
import jwt
from typing import Optional
from fastapi.security import HTTPAuthorizationCredentials
import resend
from email_templates import get_resume_conversion_email_template

logger = logging.getLogger(__name__)

# Initialize Resend API key
resend.api_key = None  # Set Resend API key here

def get_email_from_jwt(credentials: HTTPAuthorizationCredentials) -> Optional[str]:
    """
    Extract email from JWT token.
    
    Args:
        credentials: JWT credentials from FastAPI
        
    Returns:
        Optional[str]: Email if found in JWT, None otherwise
    """
    try:
        secret = None  # Set Supabase JWKS secret here
        if not secret:
            logger.error("SUPABASE_JWKS_SECRET not set")
            return None
            
        token = credentials.credentials
        payload = jwt.decode(token, secret, algorithms=["HS256"], options={"verify_aud": False})
        email = payload.get("email")
        
        if not email:
            logger.warning("No email found in JWT token")
            return None
            
        return email
    except Exception as e:
        logger.error(f"Error extracting email from JWT: {e}")
        return None

async def send_resume_conversion_email(
    user_email: str, 
    resume_link: str, 
    conversion_type: str = "resume"
) -> bool:
    """
    Send email notification after successful resume conversion.
    
    Args:
        user_email: User's email address
        resume_link: Public URL to the generated PDF
        conversion_type: Type of conversion ("resume" or "json")
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Get email template
        subject, html_content = get_resume_conversion_email_template(
            resume_link=resume_link,
            conversion_type=conversion_type
        )
        
        # Send email using Resend
        params = {
            "from": "YourApp <noreply@yourdomain.com>",  # Configure sender email here
            "to": [user_email],
            "subject": subject,
            "html": html_content,
        }
        response = resend.Emails.send(params)
        
        logger.info(f"Email sent successfully to {user_email}. Response: {response}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {user_email}: {e}")
        return False

async def send_resume_conversion_notification(
    credentials: HTTPAuthorizationCredentials,
    resume_link: str, 
    conversion_type: str = "resume"
) -> bool:
    """
    Main function to send resume conversion notification.
    Extracts email from JWT token and sends the notification.
    
    Args:
        credentials: JWT credentials from FastAPI
        resume_link: Public URL to the generated PDF
        conversion_type: Type of conversion ("resume" or "json")
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Get user email from JWT
        user_email = get_email_from_jwt(credentials)
        
        if not user_email:
            logger.warning("No email found in JWT token")
            return False
        
        # Send email
        return await send_resume_conversion_email(
            user_email=user_email,
            resume_link=resume_link,
            conversion_type=conversion_type
        )
        
    except Exception as e:
        logger.error(f"Error in send_resume_conversion_notification: {e}")
        return False
