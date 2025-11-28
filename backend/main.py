"""
FINAP Backend - Main Application Entry Point

This is the FastAPI application entry point for FINAP.
Based on architecture defined in docs/ARCHITECTURE.md
"""

import sys
import os

# Fix Windows UTF-8 encoding for emojis
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application metadata
APP_NAME = os.getenv("APP_NAME", "FINAP API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ENV = os.getenv("ENV", "development")

# CORS origins
ALLOWED_ORIGINS = [
    "http://localhost:19006",  # Expo dev server
    "http://localhost:3000",   # Web dev
    "http://localhost:3001",   # Web dev (Vite alternative port)
    "http://localhost:3002",   # Web dev (Vite alternative port 2)
    "http://localhost:3003",   # Web dev (Vite alternative port 3)
    "exp://",                  # Expo Go
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    Handles startup and shutdown logic.
    """
    # Startup
    print(f"🚀 Starting {APP_NAME} v{APP_VERSION}")
    print(f"📝 Environment: {ENV}")
    print(f"🐛 Debug mode: {DEBUG}")

    # Initialize Firebase
    from core.database import init_firebase
    init_firebase()

    # TODO: Initialize Sentry (if configured)

    yield

    # Shutdown
    print("👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    debug=DEBUG,
    lifespan=lifespan,
    docs_url="/docs" if DEBUG else None,  # Disable docs in production
    redoc_url="/redoc" if DEBUG else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    Used by load balancers and monitoring systems.
    """
    return {
        "status": "healthy",
        "version": APP_VERSION,
        "environment": ENV,
    }


@app.get("/")
async def root():
    """
    Root endpoint.
    Returns basic API information.
    """
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "docs": "/docs" if DEBUG else "disabled",
        "health": "/health",
    }


# Include routers
from api.routes import auth, fim, transactions, dashboard, whatsapp, gamification, learning, analytics

# Authentication routes (no auth required)
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["authentication"]
)

# FIM AI Assistant routes (requires auth)
app.include_router(
    fim.router,
    prefix="/api/v1/fim",
    tags=["fim-assistant"]
)

app.include_router(
    transactions.router,
    prefix="/api/v1/transactions",
    tags=["transactions"]
)

app.include_router(
    dashboard.router,
    prefix="/api/v1/dashboard",
    tags=["dashboard"]
)

app.include_router(
    whatsapp.router,
    prefix="/api/v1/whatsapp",
    tags=["whatsapp"]
)

app.include_router(
    gamification.router,
    prefix="/api/v1/gamification",
    tags=["gamification"]
)

app.include_router(
    learning.router,
    prefix="/api/v1/learning",
    tags=["learning"]
)

app.include_router(
    analytics.router,
    prefix="/api/v1/analytics",
    tags=["analytics"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=DEBUG,
    )
