"""
Script to check and diagnose Vini's balance calculation
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path to import core modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import get_firestore_client
from services.transaction_service import TransactionService
import asyncio


async def check_vini_balance():
    """Check Vini's balance and transactions"""

    print("🔍 Checking vini@email.com balance and transactions...")

    # Get Firestore client
    db = get_firestore_client()
    transaction_service = TransactionService()

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

    user_id = user_doc.id
    user_data = user_doc.to_dict()
    profile = user_data.get('profile', {})

    print(f"✅ Found user: {user_id}")
    print(f"\n📊 User Profile:")
    print(f"  - Monthly Budget: {profile.get('monthly_budget', 'NOT SET (defaults to 3000)')}")
    print(f"  - Monthly Income: {profile.get('monthly_income', 'NOT SET')}")

    # Get transactions for last 30 days
    now = datetime.now()
    start_date = now - timedelta(days=30)

    summary = await transaction_service.get_summary(
        user_id=user_id,
        start_date=start_date,
        end_date=now
    )

    print(f"\n💰 Financial Summary (Last 30 days):")
    print(f"  - Total Income: R$ {summary['total_income']:.2f}")
    print(f"  - Total Expenses: R$ {summary['total_expenses']:.2f}")
    print(f"  - Balance: R$ {summary['balance']:.2f}")
    print(f"  - Savings Rate: {summary['savings_rate']:.2f}%")
    print(f"  - Transaction Count: {summary['transaction_count']}")

    print(f"\n📈 Budget Analysis:")
    monthly_budget = profile.get('monthly_budget', 3000.0)
    spent_this_month = summary['total_expenses']
    budget_percentage = int((spent_this_month / monthly_budget) * 100) if monthly_budget > 0 else 0

    print(f"  - Monthly Budget: R$ {monthly_budget:.2f}")
    print(f"  - Spent This Month: R$ {spent_this_month:.2f}")
    print(f"  - Budget Used: {budget_percentage}%")
    print(f"  - Remaining: R$ {monthly_budget - spent_this_month:.2f}")

    print(f"\n📦 Category Breakdown:")
    for cat in summary['categories']:
        print(f"  - {cat.category}: R$ {cat.total:.2f} ({cat.percentage:.1f}%)")

    # Get actual transactions to verify
    transactions = await transaction_service.get_transactions(
        user_id=user_id,
        start_date=start_date,
        end_date=now,
        limit=100
    )

    print(f"\n📝 Recent Transactions ({len(transactions)} total):")
    for t in transactions[:10]:  # Show last 10
        symbol = "+" if t.type.value == "income" else "-"
        print(f"  {symbol} R$ {t.amount:.2f} - {t.description} ({t.category}) - {t.date.strftime('%Y-%m-%d')}")


if __name__ == "__main__":
    asyncio.run(check_vini_balance())
