"""
Script to cleanup old transactions and create realistic data for vini@email.com
Run this script from the backend directory.
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from firebase_admin import auth as firebase_auth
from core.database import init_firebase, get_firestore_client


def get_user_by_email(email: str):
    """Get user UID by email"""
    try:
        user = firebase_auth.get_user_by_email(email)
        return user.uid
    except Exception as e:
        print(f"Error getting user: {e}")
        return None


def cleanup_transactions(user_id: str):
    """Delete all existing transactions for a user"""
    db = get_firestore_client()

    print(f"🗑️  Deleting old transactions...")

    # Get all transactions for the user
    docs = db.collection('transactions').where('user_id', '==', user_id).stream()

    deleted_count = 0
    for doc in docs:
        doc.reference.delete()
        deleted_count += 1

    print(f"✅ Deleted {deleted_count} old transactions")


def create_realistic_transactions(user_id: str):
    """Create 8 realistic transactions for a young intern"""
    db = get_firestore_client()

    now = datetime.now()

    # Realistic transactions for a R$ 3000/month intern
    transactions = [
        {
            'type': 'income',
            'category': 'Receita',
            'description': 'Salário estágio',
            'amount': 3000.00,
            'date': now - timedelta(days=25),
        },
        {
            'type': 'expense',
            'category': 'Alimentação',
            'description': 'Supermercado',
            'amount': 280.00,
            'date': now - timedelta(days=20),
        },
        {
            'type': 'expense',
            'category': 'Transporte',
            'description': 'Uber para faculdade',
            'amount': 45.00,
            'date': now - timedelta(days=15),
        },
        {
            'type': 'expense',
            'category': 'Lazer',
            'description': 'Cinema com amigos',
            'amount': 60.00,
            'date': now - timedelta(days=12),
        },
        {
            'type': 'expense',
            'category': 'Alimentação',
            'description': 'iFood - Jantar',
            'amount': 35.00,
            'date': now - timedelta(days=8),
        },
        {
            'type': 'expense',
            'category': 'Educação',
            'description': 'Livro técnico',
            'amount': 89.00,
            'date': now - timedelta(days=5),
        },
        {
            'type': 'expense',
            'category': 'Lazer',
            'description': 'Netflix',
            'amount': 29.90,
            'date': now - timedelta(days=3),
        },
        {
            'type': 'expense',
            'category': 'Transporte',
            'description': 'Gasolina',
            'amount': 150.00,
            'date': now - timedelta(days=1),
        },
    ]

    print(f"💾 Creating {len(transactions)} realistic transactions...")

    for transaction in transactions:
        # Generate a unique ID for the transaction
        doc_ref = db.collection('transactions').document()
        transaction['id'] = doc_ref.id
        transaction['user_id'] = user_id
        transaction['created_at'] = datetime.now()
        doc_ref.set(transaction)

    print(f"✅ Successfully created {len(transactions)} transactions!")

    # Calculate and display summary
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    balance = total_income - total_expenses

    print(f"\n📊 Summary:")
    print(f"  Total Income:   R$ {total_income:,.2f}")
    print(f"  Total Expenses: R$ {total_expenses:,.2f}")
    print(f"  Balance:        R$ {balance:,.2f}")


def main():
    print("🚀 Initializing Firebase...")
    init_firebase()

    email = "vini@email.com"
    print(f"\n🔍 Looking for user: {email}")

    user_id = get_user_by_email(email)

    if not user_id:
        print(f"❌ User not found: {email}")
        print("Please make sure the user is registered first.")
        return

    print(f"✅ Found user with UID: {user_id}")

    # Cleanup old transactions
    cleanup_transactions(user_id)

    # Create new realistic transactions
    create_realistic_transactions(user_id)

    print(f"\n✨ Done! You can now view the updated transactions in the app.")


if __name__ == "__main__":
    main()
