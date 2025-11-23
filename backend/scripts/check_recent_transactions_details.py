"""
Script to check recent transaction details and compare to current time
"""

import sys
import os
from datetime import datetime

# Add parent directory to path to import core modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import get_firestore_client


def check_recent_transactions():
    """Check recent transactions timing details"""

    print("🔍 Checking recent transaction timing...")
    print(f"Current server time: {datetime.now()}\n")

    # Get Firestore client
    db = get_firestore_client()

    # Find vini user
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

    user_id = user_doc.id

    # Get Burger King and Sushi Night transactions
    transactions_ref = db.collection('transactions')
    query = transactions_ref.where('user_id', '==', user_id)
    docs = query.stream()

    print(f"Looking for Burger King and Sushi Night transactions:\n")

    for doc in docs:
        data = doc.to_dict()
        description = data.get('description', '')

        if 'Burger' in description or 'Sushi' in description:
            print(f"📋 Transaction: {description}")
            print(f"   Document ID: {doc.id}")
            print(f"   Amount: R$ {data.get('amount', 0):.2f}")

            date = data.get('date')
            if date:
                print(f"   Date (raw): {date}")
                print(f"   Date (type): {type(date)}")

                if hasattr(date, 'strftime'):
                    date_str = date.strftime('%Y-%m-%d %H:%M:%S')
                    print(f"   Date (formatted): {date_str}")

                    # Check timezone info
                    if hasattr(date, 'tzinfo'):
                        print(f"   Timezone info: {date.tzinfo}")

                    # Compare to now
                    now = datetime.now()
                    if hasattr(date, 'replace'):
                        date_naive = date.replace(tzinfo=None)
                        diff = date_naive - now
                        print(f"   Time difference from now: {diff}")
                        if diff.total_seconds() > 0:
                            print(f"   ⚠️ THIS TRANSACTION IS IN THE FUTURE!")
                        else:
                            print(f"   ✅ This transaction is in the past")
            else:
                print(f"   Date: NONE")

            # Check created_at
            created_at = data.get('created_at')
            if created_at:
                print(f"   Created at: {created_at}")

            print()


if __name__ == "__main__":
    check_recent_transactions()
