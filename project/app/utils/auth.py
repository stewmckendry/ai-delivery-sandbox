import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    expected_token = os.getenv("API_KEY")
    if not expected_token or credentials.credentials != expected_token:
        raise HTTPException(status_code=403, detail="Invalid or missing token")