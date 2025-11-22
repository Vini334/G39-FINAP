"""
Authentication Dependencies
FastAPI dependencies for protecting routes and getting current user.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from core.security import verify_token
from services.auth_service import AuthService

# HTTP Bearer token scheme
security = HTTPBearer()

# Auth service instance
auth_service = AuthService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Get current authenticated user from JWT token.

    This dependency extracts the JWT token from the Authorization header,
    verifies it, and returns the user_id.

    Args:
        credentials: HTTP Bearer credentials from header

    Returns:
        user_id: Authenticated user ID

    Raises:
        HTTPException: If token is invalid or missing
    """
    token = credentials.credentials

    # Verify token and extract user_id
    user_id = verify_token(token, token_type="access")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[str]:
    """
    Get current user if authenticated, or None if not.

    This is useful for endpoints that work differently for authenticated users
    but don't require authentication.

    Args:
        credentials: Optional HTTP Bearer credentials

    Returns:
        user_id or None
    """
    if credentials is None:
        return None

    token = credentials.credentials
    user_id = verify_token(token, token_type="access")

    return user_id


async def get_current_active_user(
    user_id: str = Depends(get_current_user)
) -> dict:
    """
    Get current active user's full data.

    This dependency not only verifies the token but also fetches
    the user's data from the database.

    Args:
        user_id: User ID from token

    Returns:
        User data dictionary

    Raises:
        HTTPException: If user not found or inactive
    """
    user_data = await auth_service.get_user_by_id(user_id)

    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user_data.get('is_active', True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user_data
