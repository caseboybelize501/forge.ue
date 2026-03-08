"""
Auth API — Level 7 Server API

JWT and API key authentication.

Dependencies:
- contracts.models.game_brief (L0-001)
- contracts.api.yaml (L0-008)
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import jwt

router = APIRouter(prefix="/api/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/token")
async def get_token(username: str, password: str):
    """
    Get JWT token.
    
    Args:
        username: Username
        password: Password
        
    Returns:
        JWT token
    """
    pass


@router.post("/verify")
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify JWT token.
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        Token validation result
    """
    pass
