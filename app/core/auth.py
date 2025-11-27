from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.core.config import settings

security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    # Very small demo auth; use proper hashing and secure storage in prod.
    if credentials.username == settings.API_USER and credentials.password == settings.API_PASSWORD:
        # attach a role for demonstration
        return {"username": credentials.username, "role": "viewer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
