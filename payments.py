# /backend/payments.py
import logging
import stripe
from fastapi import Request, Header, HTTPException, status

logger = logging.getLogger(__name__)

# Configure Stripe API key
stripe.api_key = None  # Set Stripe secret key here
endpoint_secret = None  # Set Stripe webhook secret here

if not stripe.api_key:
    logger.warning("STRIPE_SECRET_KEY not found. Payment processing will be disabled.")
if not endpoint_secret:
     logger.warning("STRIPE_WEBHOOK_SECRET not found. Webhook verification will be disabled (INSECURE).")

async def handle_stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    """
    Handles incoming Stripe webhook events and verifies the signature.
    Currently just logs events without processing them since auth is not implemented.
    """
    if not stripe.api_key or not endpoint_secret:
        logger.error("Stripe keys not configured. Cannot process webhooks.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Payment system not configured."
        )

    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, endpoint_secret
        )
        logger.info(f"Received valid Stripe webhook event: {event['type']}")
    except ValueError as e:
        logger.error(f"Invalid Stripe webhook payload: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid payload"
        )
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid Stripe webhook signature: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid signature"
        )
    except Exception as e:
        logger.error(f"Error constructing Stripe event: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Webhook processing error"
        )

    # For now, just log the event type and return success
    logger.info(f"Webhook event {event['type']} received (processing disabled)")
    return {"message": "Webhook received successfully."}