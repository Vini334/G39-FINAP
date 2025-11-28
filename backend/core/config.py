"""
Configuration Settings
Application configuration using environment variables.
"""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "FINAP API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENV: str = "development"

    # API
    API_V1_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:19006",
        "http://localhost:3000",
        "exp://"
    ]

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Firebase
    FIREBASE_PROJECT_ID: str = ""
    FIREBASE_PRIVATE_KEY: str = ""
    FIREBASE_CLIENT_EMAIL: str = ""
    FIREBASE_WEB_API_KEY: str = ""  # Firebase Web API Key for REST API authentication

    # External APIs
    GEMINI_API_KEY: str = ""

    # Meta WhatsApp Business API
    META_WHATSAPP_TOKEN: str = ""
    META_WHATSAPP_PHONE_ID: str = ""
    META_WHATSAPP_API_VERSION: str = "v22.0"
    META_WHATSAPP_VERIFY_TOKEN: str = "finap_webhook_verify_token_2025"
    META_WHATSAPP_FROM_NUMBER: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env file


# Global settings instance
settings = Settings()
