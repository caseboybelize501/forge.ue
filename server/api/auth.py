"""
Auth API — Level 7 Server API

JWT and API key authentication.

Dependencies:
- contracts.models.game_brief (minimal)
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict
import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/auth", tags=["auth"])
security = HTTPBearer()

# In-memory token store (replace with database in production)
_tokens_db: Dict[str, Dict] = {}
SECRET_KEY = "forge-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Mock user database
_users_db = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}


def _create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token.

    Args:
        data: Token data
        expires_delta: Optional expiration delta

    Returns:
        JWT token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token")
async def get_token(username: str, password: str):
    """
    Get JWT token.

    Args:
        username: Username
        password: Password

    Returns:
        JWT token and user info

    Raises:
        HTTPException: If credentials invalid
    """
    # Verify credentials
    if username not in _users_db:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = _users_db[username]
    if user["password"] != password:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _create_access_token(
        data={"sub": username, "role": user["role"]},
        expires_delta=access_token_expires
    )

    # Store token
    _tokens_db[access_token] = {
        "username": username,
        "role": user["role"],
        "created_at": datetime.now(),
        "expires_at": datetime.now() + access_token_expires
    }

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": username,
        "role": user["role"]
    }


@router.post("/verify")
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify JWT token.

    Args:
        credentials: HTTP authorization credentials

    Returns:
        Token validation result

    Raises:
        HTTPException: If token invalid or expired
    """
    token = credentials.credentials

    # Check if token is in store
    if token not in _tokens_db:
        raise HTTPException(
            status_code=401,
            detail="Token not found or revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = _tokens_db[token]

    # Check expiration
    if datetime.now() > token_data["expires_at"]:
        del _tokens_db[token]
        raise HTTPException(
            status_code=401,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify JWT signature
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "valid": True,
        "username": username,
        "role": token_data["role"],
        "expires_at": token_data["expires_at"]
    }


@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Logout and revoke token.

    Args:
        credentials: HTTP authorization credentials

    Returns:
        Logout confirmation
    """
    token = credentials.credentials

    if token in _tokens_db:
        del _tokens_db[token]

    return {"message": "Logged out successfully"}


@router.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get current authenticated user.

    Args:
        credentials: HTTP authorization credentials

    Returns:
        Current user info

    Raises:
        HTTPException: If not authenticated
    """
    token = credentials.credentials

    if token not in _tokens_db:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = _tokens_db[token]
    return {
        "username": token_data["username"],
        "role": token_data["role"],
        "created_at": token_data["created_at"]
    }
