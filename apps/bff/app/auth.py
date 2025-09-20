from fastapi import Request, HTTPException
import os

ADMIN_BEARER = os.getenv("ADMIN_BEARER", "")

async def require_auth(request: Request):
    if not ADMIN_BEARER:
        return
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(401, "Missing bearer")
    token = auth.split(" ", 1)[1].strip()
    if token != ADMIN_BEARER:
        raise HTTPException(403, "Invalid bearer")
