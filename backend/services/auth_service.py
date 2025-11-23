"""
Authentication Service
Handles user registration, login, and Firebase Auth integration.
"""

from typing import Optional, Dict, Any
from datetime import datetime
import requests
from firebase_admin import auth as firebase_auth
from core.database import get_firestore_client
from core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from models.user import User, UserGamification, UserProfile
from core.config import settings


class AuthService:
    """Service for authentication operations"""

    # Firebase Identity Toolkit REST API endpoint
    FIREBASE_AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

    def __init__(self):
        self.db = None

    def _get_db(self):
        """Lazy load Firestore client"""
        if self.db is None:
            self.db = get_firestore_client()
        return self.db

    def _verify_password_with_firebase(self, email: str, password: str) -> bool:
        """
        Verify user password using Firebase Auth REST API.

        Args:
            email: User email
            password: User password

        Returns:
            True if password is correct, False otherwise
        """
        try:
            # Prepare request to Firebase Auth REST API
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }

            # Make request to Firebase
            response = requests.post(
                f"{self.FIREBASE_AUTH_URL}?key={settings.FIREBASE_WEB_API_KEY}",
                json=payload,
                timeout=30  # Increased timeout to 30 seconds
            )

            print(f"DEBUG - Firebase Auth Response Status: {response.status_code}")

            # If status code is 200, password is correct
            if response.status_code == 200:
                print(f"DEBUG - Password verification successful for {email}")
                return True

            # If status code is 400, check error details
            if response.status_code == 400:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', '')
                print(f"DEBUG - Firebase Auth 400 Error: {error_message}")

                # Common Firebase Auth errors
                if 'INVALID_PASSWORD' in error_message:
                    return False
                elif 'EMAIL_NOT_FOUND' in error_message:
                    return False
                elif 'USER_DISABLED' in error_message:
                    raise Exception("Conta de usuário desativada")
                elif 'TOO_MANY_ATTEMPTS_TRY_LATER' in error_message:
                    raise Exception("Muitas tentativas de login. Tente novamente mais tarde")

            # If status code is 403, likely Identity Toolkit API disabled
            if response.status_code == 403:
                error_data = response.json()
                print(f"DEBUG - Firebase Auth Response: {error_data}")
                raise Exception(f"Error verifying password: {error_data.get('error', {}).get('message', 'Service disabled')}")

            # Other errors
            print(f"DEBUG - Unexpected Firebase Auth response: {response.status_code}")
            return False

        except requests.exceptions.RequestException as e:
            print(f"DEBUG - Request exception: {str(e)}")
            raise Exception(f"Error verifying password: {str(e)}")
        except Exception as e:
            # If it's already our custom exception, re-raise it
            if "Error verifying password:" in str(e):
                raise
            print(f"DEBUG - Unexpected exception: {str(e)}")
            raise Exception(f"Error verifying password: {str(e)}")

    async def register_user(
        self,
        email: str,
        password: str,
        name: str,
        phone: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register a new user with Firebase Auth and create Firestore profile.

        Args:
            email: User email
            password: User password (plain text)
            name: User full name
            phone: Optional phone number

        Returns:
            Dictionary with user data and tokens

        Raises:
            Exception: If user already exists or registration fails
        """
        db = self._get_db()

        try:
            # 1. Create Firebase Auth user
            firebase_user = firebase_auth.create_user(
                email=email,
                password=password,
                display_name=name,
                phone_number=phone if phone else None
            )

            user_id = firebase_user.uid

            # 2. Create user profile in Firestore
            now = datetime.utcnow()

            # Initial gamification stats
            gamification = UserGamification(
                level=1,
                xp=0,
                coins=100,  # Welcome bonus
                lives=5,
                badges=[],
                current_streak=0,
                longest_streak=0,
                last_login=now
            )

            # Initial profile
            profile = UserProfile(
                age=None,
                monthly_income=None,
                financial_goals=[],
                avatar_url=None
            )

            # Create user document
            user_data = {
                "uid": user_id,
                "email": email,
                "name": name,
                "phone": phone,
                "created_at": now,
                "updated_at": now,
                "is_active": True,
                "is_premium": False,
                "profile": profile.dict(),
                "gamification": gamification.dict(),
                "preferences": {
                    "notifications": True,
                    "dark_mode": False,
                    "language": "pt-BR",
                    "currency": "BRL"
                }
            }

            db.collection('users').document(user_id).set(user_data)

            # 3. Generate JWT tokens
            access_token = create_access_token(data={"sub": user_id})
            refresh_token = create_refresh_token(data={"sub": user_id})

            # 4. Return user data and tokens
            return {
                "user": {
                    "uid": user_id,
                    "email": email,
                    "name": name,
                    "gamification": gamification.dict()
                },
                "tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer"
                }
            }

        except firebase_auth.EmailAlreadyExistsError:
            raise Exception("Email already registered")
        except Exception as e:
            raise Exception(f"Registration failed: {str(e)}")

    async def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user with email (password verification temporarily disabled).

        Args:
            email: User email
            password: User password (not validated for now)

        Returns:
            Dictionary with user data and tokens

        Raises:
            Exception: If user not found or inactive
        """
        db = self._get_db()

        try:
            # 1. Get user by email from Firebase Auth
            try:
                firebase_user = firebase_auth.get_user_by_email(email)
                user_id = firebase_user.uid
            except firebase_auth.UserNotFoundError:
                raise Exception("Email não encontrado. Por favor, cadastre-se primeiro.")

            # 2. Get user data from Firestore
            user_doc = db.collection('users').document(user_id).get()

            if not user_doc.exists:
                raise Exception("Usuário não encontrado no banco de dados")

            user_data = user_doc.to_dict()

            # Check if user is active
            if not user_data.get('is_active', True):
                raise Exception("Conta de usuário desativada")

            # NOTE: Password verification is temporarily disabled for development
            # Will be implemented later with proper authentication
            print(f"⚠️  LOGIN: Password verification is disabled - allowing login for {email}")

            # 3. Update last login
            now = datetime.utcnow()
            db.collection('users').document(user_id).update({
                'gamification.last_login': now
            })

            # 4. Generate tokens
            access_token = create_access_token(data={"sub": user_id})
            refresh_token = create_refresh_token(data={"sub": user_id})

            return {
                "user": {
                    "uid": user_id,
                    "email": user_data.get('email'),
                    "name": user_data.get('name'),
                    "gamification": user_data.get('gamification', {})
                },
                "tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer"
                }
            }

        except Exception as e:
            # If it's already a custom exception, re-raise it
            if "não encontrado" in str(e) or "desativada" in str(e) or "cadastre-se" in str(e):
                raise
            raise Exception(f"Erro ao fazer login: {str(e)}")

    async def refresh_access_token(self, refresh_token: str) -> Dict[str, str]:
        """
        Generate new access token from refresh token.

        Args:
            refresh_token: Valid refresh token

        Returns:
            Dictionary with new access token

        Raises:
            Exception: If refresh token is invalid
        """
        from core.security import verify_token

        # Verify refresh token
        user_id = verify_token(refresh_token, token_type="refresh")

        if not user_id:
            raise Exception("Invalid or expired refresh token")

        # Generate new access token
        access_token = create_access_token(data={"sub": user_id})

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user data by user ID.

        Args:
            user_id: Firebase user ID

        Returns:
            User data dictionary or None if not found
        """
        db = self._get_db()

        user_doc = db.collection('users').document(user_id).get()

        if not user_doc.exists:
            return None

        return user_doc.to_dict()

    async def update_user_profile(
        self,
        user_id: str,
        update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Update user profile information.

        Args:
            user_id: User ID
            update_data: Dictionary with fields to update

        Returns:
            Updated user data or None if user not found
        """
        db = self._get_db()

        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return None

        # Update fields
        update_data['updated_at'] = datetime.utcnow()
        user_ref.update(update_data)

        # Get updated data
        updated_doc = user_ref.get()
        return updated_doc.to_dict()

    async def delete_user(self, user_id: str) -> bool:
        """
        Delete user account from Firebase Auth and Firestore.

        Args:
            user_id: User ID

        Returns:
            True if deleted successfully
        """
        db = self._get_db()

        try:
            # Delete from Firebase Auth
            firebase_auth.delete_user(user_id)

            # Delete from Firestore
            db.collection('users').document(user_id).delete()

            return True

        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            return False
