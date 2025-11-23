"""
Script to update Vini user stats
Updates streak to 5 and coins to 900 for vini@email.com
"""

import sys
import os

# Add parent directory to path to import core modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import get_firestore_client


def update_vini_stats():
    """Update vini@email.com user stats"""

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
    print(f"\n📊 Current stats:")
    print(f"  - Current Streak: {user_data.get('gamification', {}).get('current_streak', 0)}")
    print(f"  - Coins: {user_data.get('gamification', {}).get('coins', 0)}")

    # Update gamification data
    update_data = {
        'gamification.current_streak': 5,
        'gamification.coins': 900
    }

    # Update in Firestore
    user_doc.reference.update(update_data)

    print(f"\n✅ Updated stats:")
    print(f"  - Current Streak: 5")
    print(f"  - Coins: 900")
    print(f"\n🎉 User stats updated successfully!")


if __name__ == "__main__":
    update_vini_stats()
