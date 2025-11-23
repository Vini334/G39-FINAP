"""
Script to test Firestore query and diagnose the issue
"""

import sys
import os

# Add parent directory to path to import core modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import get_firestore_client


def test_query():
    """Test the simple user_id query"""

    print("🔍 Testing Firestore query...")

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

    # Test the simple query
    print(f"\n🔍 Testing transactions query for user_id={user_id}")

    try:
        transactions_ref = db.collection('transactions')
        query = transactions_ref.where('user_id', '==', user_id)

        print("📋 Executing query...")
        docs = query.stream()

        transactions = []
        for doc in docs:
            data = doc.to_dict()
            transactions.append(data)
            print(f"  ✓ Found transaction: {data.get('description', 'N/A')} - R$ {data.get('amount', 0)}")

        print(f"\n✅ Query succeeded! Found {len(transactions)} transactions")

        # Calculate totals
        total_expenses = sum(t['amount'] for t in transactions if t.get('type') == 'expense')
        total_income = sum(t['amount'] for t in transactions if t.get('type') == 'income')

        print(f"\n💰 Totals:")
        print(f"  - Total Expenses: R$ {total_expenses:.2f}")
        print(f"  - Total Income: R$ {total_income:.2f}")
        print(f"  - Balance: R$ {total_income - total_expenses:.2f}")

    except Exception as e:
        print(f"❌ Query failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_query()
