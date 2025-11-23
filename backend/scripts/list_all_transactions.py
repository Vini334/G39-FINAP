"""
Script to list all transactions and check which user they belong to
"""

import sys
import os
from datetime import datetime

# Add parent directory to path to import core modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import get_firestore_client


def list_all_transactions():
    """List all transactions in the database"""

    print("🔍 Listing all transactions in database...")

    # Get Firestore client
    db = get_firestore_client()

    # Get all transactions
    transactions_ref = db.collection('transactions')
    docs = transactions_ref.order_by('date', direction='DESCENDING').limit(20).stream()

    print(f"\n📝 Last 20 Transactions:\n")
    print(f"{'User ID':<40} {'Date':<25} {'Type':<10} {'Amount':<10} {'Description':<30} {'Category':<15}")
    print("=" * 140)

    count = 0
    for doc in docs:
        data = doc.to_dict()
        user_id = data.get('user_id', 'N/A')
        date = data.get('date')
        if date:
            date_str = date.strftime('%Y-%m-%d %H:%M:%S') if hasattr(date, 'strftime') else str(date)
        else:
            date_str = 'N/A'
        tx_type = data.get('type', 'N/A')
        amount = data.get('amount', 0)
        description = data.get('description', 'N/A')[:30]
        category = data.get('category', 'N/A')

        print(f"{user_id:<40} {date_str:<25} {tx_type:<10} R$ {amount:<8.2f} {description:<30} {category:<15}")
        count += 1

    print(f"\n✅ Total transactions shown: {count}")

    # Show user count
    print(f"\n👥 Checking users...")
    users_ref = db.collection('users')
    users = users_ref.stream()

    print(f"\n{'Email':<30} {'User ID':<40}")
    print("=" * 70)
    for user in users:
        user_data = user.to_dict()
        email = user_data.get('email', 'N/A')
        print(f"{email:<30} {user.id:<40}")


if __name__ == "__main__":
    list_all_transactions()
