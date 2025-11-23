"""
Script to check transaction dates for vini user
"""

import sys
import os
from datetime import datetime

# Add parent directory to path to import core modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import get_firestore_client


def check_transaction_dates():
    """Check dates of all transactions for vini user"""

    print("🔍 Checking transaction dates...")

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
    print(f"✅ Found user: {user_id}")

    # Get all transactions
    transactions_ref = db.collection('transactions')
    query = transactions_ref.where('user_id', '==', user_id)
    docs = query.stream()

    print(f"\n📋 All Transactions:\n")
    print(f"{'Description':<30} {'Amount':<12} {'Type':<10} {'Date':<30}")
    print("=" * 82)

    now = datetime.now()
    from datetime import timedelta
    start_date = now - timedelta(days=30)

    for doc in docs:
        data = doc.to_dict()
        description = data.get('description', 'N/A')[:30]
        amount = data.get('amount', 0)
        tx_type = data.get('type', 'N/A')
        date = data.get('date')

        if date:
            date_str = date.strftime('%Y-%m-%d %H:%M:%S') if hasattr(date, 'strftime') else str(date)

            # Check if within range
            in_range = ""
            if hasattr(date, 'replace'):
                date_naive = date.replace(tzinfo=None)
                start_naive = start_date.replace(tzinfo=None)
                now_naive = now.replace(tzinfo=None)

                if start_naive <= date_naive <= now_naive:
                    in_range = "✅ IN RANGE"
                else:
                    in_range = "❌ OUT OF RANGE"
        else:
            date_str = 'N/A'
            in_range = "⚠️ NO DATE"

        print(f"{description:<30} R$ {amount:<9.2f} {tx_type:<10} {date_str:<30} {in_range}")

    print(f"\n📅 Date range being used:")
    print(f"  Start: {start_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  End:   {now.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    check_transaction_dates()
