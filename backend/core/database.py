"""
Database Configuration
Firebase Firestore initialization and connection.
"""

import sys
import firebase_admin
from firebase_admin import credentials, firestore
from core.config import settings
import json
import os
from pathlib import Path
from typing import Optional

# Fix Windows UTF-8 encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass


# Global Firestore client
_db_client: Optional[firestore.Client] = None


def init_firebase():
    """
    Initialize Firebase Admin SDK.
    Should be called during app startup.
    """
    global _db_client

    if _db_client is not None:
        return _db_client

    try:
        # Check if Firebase is already initialized
        firebase_admin.get_app()
    except ValueError:
        # Try to load credentials from JSON file first
        # Path is: backend/core/database.py -> go up to backend -> then to project root -> then credentials
        credentials_path = Path(__file__).parent.parent / ".." / "credentials" / "firebase-service-account.json"
        credentials_path = credentials_path.resolve()  # Resolve to absolute path

        if credentials_path.exists():
            try:
                cred = credentials.Certificate(str(credentials_path))
                firebase_admin.initialize_app(cred)
                print("✅ Firebase initialized successfully from credentials file")
            except Exception as e:
                print(f"❌ Failed to initialize Firebase from file: {str(e)}")
                print("⚠️  Using mock data mode. Check your Firebase credentials")
                return None
        # Fallback to environment variables
        elif settings.FIREBASE_PRIVATE_KEY and settings.FIREBASE_CLIENT_EMAIL:
            try:
                # Parse private key (handle newlines)
                private_key = settings.FIREBASE_PRIVATE_KEY.replace('\\n', '\n')

                cred_dict = {
                    "type": "service_account",
                    "project_id": settings.FIREBASE_PROJECT_ID,
                    "private_key": private_key,
                    "client_email": settings.FIREBASE_CLIENT_EMAIL,
                    "token_uri": "https://oauth2.googleapis.com/token",
                }

                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
                print("✅ Firebase initialized successfully from environment variables")
            except Exception as e:
                print(f"❌ Failed to initialize Firebase from env vars: {str(e)}")
                print("⚠️  Using mock data mode. Check your Firebase credentials in .env")
                return None
        else:
            print("⚠️  Firebase credentials not configured. Using mock data.")
            return None

    _db_client = firestore.client()
    return _db_client


def get_firestore_client() -> firestore.Client:
    """
    Get Firestore client instance.

    Returns:
        Firestore client instance

    Raises:
        RuntimeError: If Firebase is not initialized
    """
    global _db_client

    if _db_client is None:
        _db_client = init_firebase()

    if _db_client is None:
        raise RuntimeError(
            "Firebase not initialized. Check your credentials in .env file."
        )

    return _db_client


def close_firebase():
    """
    Close Firebase connection.
    Should be called during app shutdown.
    """
    global _db_client
    _db_client = None
    # Firebase Admin SDK handles cleanup automatically
