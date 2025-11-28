"""
Authentication Schemas
Request and response models for authentication endpoints.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Dict, Any
import re


class RegisterRequest(BaseModel):
    """User registration request"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ...,
        min_length=6,
        description="Password (min 6 characters, 1 uppercase, 1 number)"
    )
    name: str = Field(..., min_length=2, description="Full name")
    phone: Optional[str] = Field(None, description="Phone number (optional)")
    monthly_income: Optional[float] = Field(None, description="Monthly income (R$)")
    savings_goal: Optional[float] = Field(None, description="Monthly savings goal (R$)")

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Validate password strength:
        - Minimum 6 characters
        - At least 1 uppercase letter
        - At least 1 number
        """
        if len(v) < 6:
            raise ValueError('Senha deve ter no mínimo 6 caracteres')

        if not re.search(r'[A-Z]', v):
            raise ValueError('Senha deve conter pelo menos uma letra maiúscula')

        if not re.search(r'\d', v):
            raise ValueError('Senha deve conter pelo menos um número')

        return v

    class Config:
        json_schema_extra = {
            "example": {
                "email": "joao@example.com",
                "password": "SecurePass123",
                "name": "João Silva",
                "phone": "+5511999999999"
            }
        }


class LoginRequest(BaseModel):
    """User login request"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "joao@example.com",
                "password": "SecurePass123"
            }
        }


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str = Field(..., description="Valid refresh token")

    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class TokenResponse(BaseModel):
    """JWT tokens response"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: Optional[str] = Field(None, description="JWT refresh token (on login/register)")
    token_type: str = Field(default="bearer", description="Token type")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class UserResponse(BaseModel):
    """User data response"""
    uid: str = Field(..., description="User unique ID")
    email: str = Field(..., description="User email")
    name: str = Field(..., description="User name")
    gamification: Optional[Dict[str, Any]] = Field(None, description="Gamification stats")

    class Config:
        json_schema_extra = {
            "example": {
                "uid": "abc123xyz",
                "email": "joao@example.com",
                "name": "João Silva",
                "gamification": {
                    "level": 1,
                    "xp": 0,
                    "coins": 100,
                    "lives": 5
                }
            }
        }


class AuthResponse(BaseModel):
    """Complete authentication response"""
    user: UserResponse
    tokens: TokenResponse

    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "uid": "abc123xyz",
                    "email": "joao@example.com",
                    "name": "João Silva",
                    "gamification": {
                        "level": 1,
                        "xp": 0,
                        "coins": 100
                    }
                },
                "tokens": {
                    "access_token": "eyJhbGc...",
                    "refresh_token": "eyJhbGc...",
                    "token_type": "bearer"
                }
            }
        }


class UpdateProfileRequest(BaseModel):
    """Update user profile request"""
    name: Optional[str] = Field(None, min_length=2, description="Full name")
    phone: Optional[str] = Field(None, description="Phone number")
    profile: Optional[Dict[str, Any]] = Field(None, description="Profile data")
    preferences: Optional[Dict[str, Any]] = Field(None, description="User preferences")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "João da Silva Santos",
                "profile": {
                    "age": 25,
                    "monthly_income": 3000.00
                },
                "preferences": {
                    "dark_mode": True,
                    "notifications": False
                }
            }
        }
