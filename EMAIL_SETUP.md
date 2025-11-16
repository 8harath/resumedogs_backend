# Email Integration Setup

This document explains the email functionality that has been added to send notifications after resume conversion.

## Files Added

1. **`email_service.py`** - Main email service module with Resend integration
2. **`email_templates.py`** - HTML email templates for notifications
3. **`EMAIL_SETUP.md`** - This setup guide

## Dependencies Added

- `resend==0.8.0` - Added to `requirements.txt`

## Environment Variables Required

Add this to your `.env` file:

```env
# RESEND_API_KEY=your_resend_api_key_here
```

## How It Works

1. **After successful resume conversion** (both `/convert-latex` and `/convert-json-to-latex` endpoints):
   - The system extracts the user's email directly from the JWT token
   - Sends a professional HTML email with a download link to the generated PDF
   - Email sending is non-blocking - if it fails, the main request still succeeds

2. **Email Features**:
   - Professional HTML template with gradient header
   - Generic greeting ("Hello! 👋")
   - Direct download button for the PDF
   - Conversion details (format, type, status)
   - Pro tips for users
   - Responsive design

3. **Error Handling**:
   - If email is not found in JWT token, logs a warning but doesn't fail
   - If email sending fails, logs the error but doesn't affect the main request
   - Comprehensive logging for debugging

## Setup Steps

1. **Install the new dependency**:
   ```bash
   pip install resend==0.8.0
   ```

2. **Add Resend API key to your `.env` file**:
   ```env
   # RESEND_API_KEY=your_actual_resend_api_key
   ```

3. **Update the sender email** in `email_service.py`:
   ```python
   "from": "YourApp <noreply@yourdomain.com>",  # Configure with your verified domain
   ```

4. **Test the integration** by making a resume conversion request

## Email Template Customization

The email template is in `email_templates.py`. You can customize:
- Colors and styling
- Content and messaging
- Pro tips
- File details display

## JWT Token Requirements

The system extracts the email directly from the JWT token. The JWT should contain:
- `sub` field (user_id)
- `email` field (user's email address)

## Logging

Email sending is logged at INFO level for successful sends and WARNING/ERROR level for failures. Check your logs to monitor email delivery.

## Testing

To test the email functionality:
1. Ensure you have a valid Resend API key
2. Make sure your Supabase users table has email addresses
3. Make a resume conversion request
4. Check the logs for email sending status
5. Verify the email is received
