from fastapi import Depends, HTTPException
from .middleware.auth import verify_token


def get_current_user(token: str = Depends(verify_token)):
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"user_id": "demo-user"}