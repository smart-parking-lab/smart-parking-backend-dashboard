from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
import os

security = HTTPBearer(auto_error=False)

SECRET_KEY_ACCESS_TOKEN = os.getenv("SECRET_KEY_ACCESS_TOKEN")
ALGORITHM = os.getenv("ALGORITHM")

def verify_token(credentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY_ACCESS_TOKEN, algorithms=[ALGORITHM])
        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")