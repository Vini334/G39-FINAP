"""
Script to set monthly budget to 3000 for vini@email.com
"""

import sys
import os

# Add parent directory to path to import core modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import get_firestore_client


def set_vini_budget():
    """Set vini@email.com monthly budget to 3000"""

    print("🔍 Searching for vini@email.com...")

    # Get Firestore client
    db = get_firestore_client()

    # Query Firestore for user with email vini@email.com
    users_ref = db.collection('users')
    query = users_ref.where('email', '==', 'vini@email.com').limit(1)
    docs = query.stream()

    user_doc = None
    for doc in docs:
        user_doc = doc
        break

    if not user_doc:
        print("❌ User vini@email.com not found!")
        return

    print(f"✅ Found user: {user_doc.id}")

    # Get current data
    user_data = user_doc.to_dict()
    profile = user_data.get('profile', {})
    current_budget = profile.get('monthly_budget', 'NOT SET')

    print(f"\n📊 Current monthly budget: {current_budget}")

    # Update profile with monthly_budget = 3000
    update_data = {
        'profile.monthly_budget': 3000.0
    }

    # Update in Firestore
    user_doc.reference.update(update_data)

    print(f"\n✅ Updated monthly budget to R$ 3000.00")
    print(f"🎉 Budget successfully updated for vini@email.com!")


if __name__ == "__main__":
    set_vini_budget()
