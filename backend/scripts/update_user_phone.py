"""
Script to update user phone number in Firestore.
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import init_firebase, get_firestore_client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def update_user_phone(user_id, phone):
    """Update user phone number"""

    print("🔧 Initializing Firebase...")
    init_firebase()
    db = get_firestore_client()

    print(f"\n👤 Updating user: {user_id}")
    print(f"📱 New phone: {phone}")

    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()

    if user_doc.exists:
        user_ref.update({
            'phone': phone,
            'updated_at': datetime.now().isoformat()
        })

        print("\n✅ User updated successfully!")

        # Show updated user
        updated_doc = user_ref.get()
        user_data = updated_doc.to_dict()

        print(f"\n📝 Updated user data:")
        print(f"   Name: {user_data.get('name')}")
        print(f"   Email: {user_data.get('email')}")
        print(f"   Phone: {user_data.get('phone')}")

    else:
        print(f"\n❌ User not found: {user_id}")

if __name__ == "__main__":
    # Update with the user's real phone number
    update_user_phone('test-user-whatsapp', '+5511962830374')
