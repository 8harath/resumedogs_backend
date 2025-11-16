"""
Email templates for resume conversion notifications.
"""

def get_resume_conversion_email_template(
    resume_link: str, 
    conversion_type: str = "resume"
) -> tuple[str, str]:
    """
    Generate HTML email template for resume conversion notification.
    
    Args:
        resume_link: Public URL to the generated PDF
        conversion_type: Type of conversion ("resume" or "json")
    
    Returns:
        tuple: (subject, html_content)
    """
    subject = "Your Resume PDF is Ready! 📄"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Resume PDF Ready</title>
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #000; background: #f5f5f5; margin: 0; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: #fff; border: 3px solid #000; padding: 40px;">
            <h1 style="color: #000; margin: 0 0 20px 0; font-size: 24px; font-weight: 600;">Your Resume PDF is Ready!</h1>
            <p style="color: #000; margin: 0 0 30px 0; font-size: 16px; line-height: 1.5;">Your resume has been successfully converted to PDF. Click the button below to download:</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{resume_link}" 
                   style="background: #fff; color: #000; padding: 18px 36px; text-decoration: none; border: 3px solid #000; border-radius: 4px; font-weight: 600; display: inline-block; font-size: 16px;">
                    Download PDF Resume
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    return subject, html_content
