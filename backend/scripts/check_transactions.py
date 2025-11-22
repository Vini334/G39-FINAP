"""
Script to check recent transactions in Firestore.
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import init_firebase, get_firestore_client
from dotenv import load_dotenv
import json

load_dotenv()

def check_recent_transactions():
    """Check recent transactions"""

    print("🔧 Initializing Firebase...")
    init_firebase()
    db = get_firestore_client()

    print("\n💰 Fetching recent transactions...")

    transactions_ref = db.collection('transactions')

    # Get last 5 transactions ordered by created_at
    query = transactions_ref.order_by('created_at', direction='DESCENDING').limit(5)
    docs = query.stream()

    count = 0
    for doc in docs:
        data = doc.to_dict()
        count += 1

        print(f"\n{'='*60}")
        print(f"Transaction #{count}")
        print(f"{'='*60}")
        print(f"ID: {doc.id}")
        print(f"Type: {data.get('type')}")
        print(f"Amount: R$ {data.get('amount')}")
        print(f"Category: {data.get('category')}")
        print(f"Description: {data.get('description')}")
        print(f"Source: {data.get('source')}")
        print(f"Date: {data.get('date')}")
        print(f"Created at: {data.get('created_at')}")

    if count == 0:
        print("\n❌ No transactions found")
    else:
        print(f"\n✅ Found {count} transactions")

if __name__ == "__main__":
    check_recent_transactions()
