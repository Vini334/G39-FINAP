#!/usr/bin/env python3
"""
Create Test User Script
Creates a test user with gamification data in Firestore for development.
"""

import sys
import os
from datetime import datetime

# Fix Windows UTF-8 encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import init_firebase, get_firestore_client

def create_test_user():
    """Create test user in Firestore"""

    # Initialize Firebase
    init_firebase()
    db = get_firestore_client()

    user_id = "test-user-123"

    # User data
    user_data = {
        "phone": "5511995989872",  # Número do WhatsApp (formato que a Meta envia)
        "profile": {
            "name": "Usuário Teste",
            "email": "teste@finap.com",
            "age": 25,
            "monthly_income": 5000.0,
            "monthly_budget": 3000.0,
            "financial_goals": ["Economizar", "Investir"],
            "created_at": datetime.now()
        },
        "gamification": {
            "level": 2,
            "xp": 150,
            "lives": 5,
            "coins": 250,
            "current_streak": 3,
            "longest_streak": 5,
            "badges": [],
            "last_login": datetime.now()
        },
        "settings": {
            "notifications": True,
            "dark_mode": False,
            "language": "pt-BR"
        },
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

    # Create or update user document
    user_ref = db.collection('users').document(user_id)
    user_ref.set(user_data)

    print(f"✅ User '{user_id}' created successfully!")
    print(f"   - Phone: +{user_data['phone']}")
    print(f"   - Level: {user_data['gamification']['level']}")
    print(f"   - XP: {user_data['gamification']['xp']}")
    print(f"   - Lives: {user_data['gamification']['lives']}")
    print(f"   - Coins: {user_data['gamification']['coins']}")
    print(f"   - Streak: {user_data['gamification']['current_streak']}")
    print(f"   - Budget: R$ {user_data['profile']['monthly_budget']}")
    print(f"\n📲 Agora você pode enviar mensagens pelo WhatsApp para: +15551534852")
    print(f"💬 Teste com: 'ajuda' ou 'gastei 50 no mercado'")

    return user_id

if __name__ == "__main__":
    try:
        user_id = create_test_user()
        print(f"\n🎉 Test user ready! Use user_id: {user_id}")
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        sys.exit(1)
