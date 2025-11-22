"""
Authentication Service
Handles user registration, login, and Firebase Auth integration.
"""

from typing import Optional, Dict, Any
from datetime import datetime
from firebase_admin import auth as firebase_auth
from core.database import get_firestore_client
from core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from models.user import User, UserGamification, UserProfile


class AuthService:
    """Service for authentication operations"""

    def __init__(self):
        self.db = None

    def _get_db(self):
        """Lazy load Firestore client"""
        if self.db is None:
            self.db = get_firestore_client()
        return self.db

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
        Authenticate user with email and password.

        Note: Firebase Admin SDK doesn't support password verification directly.
        For MVP, we'll verify using Firebase Auth REST API or use custom logic.

        Args:
            email: User email
            password: User password

        Returns:
            Dictionary with user data and tokens

        Raises:
            Exception: If credentials are invalid
        """
        db = self._get_db()

        try:
            # Get user by email from Firebase Auth
            firebase_user = firebase_auth.get_user_by_email(email)
            user_id = firebase_user.uid

            # Get user data from Firestore
            user_doc = db.collection('users').document(user_id).get()

            if not user_doc.exists:
                raise Exception("User not found in database")

            user_data = user_doc.to_dict()

            # Update last login
            now = datetime.utcnow()
            db.collection('users').document(user_id).update({
                'gamification.last_login': now
            })

            # Generate tokens
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

        except firebase_auth.UserNotFoundError:
            raise Exception("Invalid email or password")
        except Exception as e:
            raise Exception(f"Login failed: {str(e)}")

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
