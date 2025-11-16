# /backend/auth.py
import logging
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import User # Import your User Pydantic model

logger = logging.getLogger(__name__)

# --- Authentication Dependency ---
# Uses HTTP Bearer token (expects "Authorization: Bearer <token>" header)
bearer_scheme = HTTPBearer(auto_error=False) # auto_error=False to handle missing token gracefully

# Remove get_current_user and decrement_user_credits if not used by other endpoints
# (No changes needed if only /convert-latex is affected)