"""
Authentication Routes
API endpoints for user registration, login, and token management.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from schemas.auth import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    AuthResponse,
    TokenResponse,
    UserResponse,
    UpdateProfileRequest
)
from schemas.common import SuccessResponse, APIResponse
from services.auth_service import AuthService
from api.dependencies.auth import get_current_user, get_current_active_user

router = APIRouter()
auth_service = AuthService()


@router.post("/register", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    """
    Register a new user account.

    **Request Body:**
    - email: Valid email address
    - password: Password (minimum 6 characters)
    - name: Full name
    - phone: Optional phone number

    **Returns:**
    - User data
    - Access token (15 min expiration)
    - Refresh token (7 days expiration)

    **Status Codes:**
    - 201: User created successfully
    - 400: Invalid data or email already exists
    """
    try:
        result = await auth_service.register_user(
            email=request.email,
            password=request.password,
            name=request.name,
            phone=request.phone
        )

        return APIResponse(
            success=True,
            data=result,
            message="User registered successfully"
        )

    except Exception as e:
        error_message = str(e)
        if "already" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message
        )


@router.post("/login", response_model=APIResponse)
async def login(request: LoginRequest):
    """
    Authenticate user and generate tokens.

    **Request Body:**
    - email: User email
    - password: User password

    **Returns:**
    - User data
    - Access token (15 min expiration)
    - Refresh token (7 days expiration)

    **Status Codes:**
    - 200: Login successful
    - 401: Invalid credentials
    """
    try:
        result = await auth_service.login(
            email=request.email,
            password=request.password
        )

        return APIResponse(
            success=True,
            data=result,
            message="Login successful"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/refresh", response_model=APIResponse)
async def refresh_token(request: RefreshTokenRequest):
    """
    Generate new access token from refresh token.

    **Request Body:**
    - refresh_token: Valid refresh token

    **Returns:**
    - New access token

    **Status Codes:**
    - 200: Token refreshed successfully
    - 401: Invalid or expired refresh token
    """
    try:
        result = await auth_service.refresh_access_token(request.refresh_token)

        return APIResponse(
            success=True,
            data=result,
            message="Token refreshed successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/logout", response_model=APIResponse)
async def logout(current_user_id: str = Depends(get_current_user)):
    """
    Logout current user.

    Note: Since we're using JWT tokens, logout is handled on the client side
    by deleting the stored tokens. This endpoint is mainly for audit/logging.

    **Headers:**
    - Authorization: Bearer {access_token}

    **Returns:**
    - Success message

    **Status Codes:**
    - 200: Logout successful
    - 401: Invalid or missing token
    """
    # In a production app, you might want to:
    # - Add token to blacklist
    # - Log logout event
    # - Clear user sessions

    return APIResponse(
        success=True,
        data={},
        message="Logged out successfully"
    )


@router.get("/me", response_model=APIResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_active_user)):
    """
    Get current authenticated user's information.

    **Headers:**
    - Authorization: Bearer {access_token}

    **Returns:**
    - Complete user profile data

    **Status Codes:**
    - 200: Success
    - 401: Invalid or missing token
    - 404: User not found
    """
    return APIResponse(
        success=True,
        data={"user": current_user},
        message="User data retrieved successfully"
    )


@router.put("/me", response_model=APIResponse)
async def update_current_user(
    request: UpdateProfileRequest,
    current_user_id: str = Depends(get_current_user)
):
    """
    Update current user's profile information.

    **Headers:**
    - Authorization: Bearer {access_token}

    **Request Body (all optional):**
    - name: New name
    - phone: New phone number
    - profile: Profile data (age, monthly_income, etc)
    - preferences: User preferences (dark_mode, notifications, etc)

    **Returns:**
    - Updated user data

    **Status Codes:**
    - 200: Profile updated successfully
    - 401: Invalid or missing token
    - 404: User not found
    """
    try:
        # Build update data
        update_data = {}

        if request.name is not None:
            update_data['name'] = request.name

        if request.phone is not None:
            update_data['phone'] = request.phone

        if request.profile is not None:
            for key, value in request.profile.items():
                update_data[f'profile.{key}'] = value

        if request.preferences is not None:
            for key, value in request.preferences.items():
                update_data[f'preferences.{key}'] = value

        # Update user
        updated_user = await auth_service.update_user_profile(
            user_id=current_user_id,
            update_data=update_data
        )

        if updated_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return APIResponse(
            success=True,
            data={"user": updated_user},
            message="Profile updated successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/me", response_model=APIResponse)
async def delete_current_user(current_user_id: str = Depends(get_current_user)):
    """
    Delete current user's account.

    **WARNING:** This action is irreversible.

    **Headers:**
    - Authorization: Bearer {access_token}

    **Returns:**
    - Success message

    **Status Codes:**
    - 200: Account deleted successfully
    - 401: Invalid or missing token
    """
    try:
        deleted = await auth_service.delete_user(current_user_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete account"
            )

        return APIResponse(
            success=True,
            data={},
            message="Account deleted successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
