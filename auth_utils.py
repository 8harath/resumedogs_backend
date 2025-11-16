import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

def get_user_id_from_jwt(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> str:
    secret = None  # Set Supabase JWKS secret here
    if not secret:
        raise HTTPException(status_code=500, detail="SUPABASE_JWKS_SECRET not set.")
    token = credentials.credentials
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"], options={"verify_aud": False})
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return user_id
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid authentication credentials: {str(e)}")
