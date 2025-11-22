"""
Script to check user data in Firestore.
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import init_firebase, get_firestore_client
from dotenv import load_dotenv
import json

load_dotenv()

def check_user(user_id):
    """Check user data"""

    print("🔧 Initializing Firebase...")
    init_firebase()
    db = get_firestore_client()

    print(f"\n👤 Fetching user: {user_id}")

    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()

    if user_doc.exists:
        user_data = user_doc.to_dict()
        print("\n✅ User found!")
        print("\n" + "="*50)
        print(json.dumps(user_data, indent=2, default=str))
        print("="*50)

        print(f"\n📱 Phone number: {user_data.get('phone')}")
        print(f"📧 Email: {user_data.get('email')}")
        print(f"👤 Name: {user_data.get('name')}")

        if 'gamification' in user_data:
            print(f"\n🎮 Gamification:")
            print(f"   Level: {user_data['gamification'].get('level')}")
            print(f"   XP: {user_data['gamification'].get('xp')}")
            print(f"   Coins: {user_data['gamification'].get('coins')}")
            print(f"   Lives: {user_data['gamification'].get('lives')}")
    else:
        print(f"\n❌ User not found: {user_id}")

if __name__ == "__main__":
    check_user('test-user-whatsapp')
