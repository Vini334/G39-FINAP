"""
Script to populate synthetic transaction data for vini@email.com user.
Run this script from the backend directory.
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from firebase_admin import auth as firebase_auth
from core.database import init_firebase, get_firestore_client


# Transaction categories with typical Brazilian expenses
CATEGORIES = {
    'Alimentação': ['Supermercado Extra', 'Padaria Central', 'iFood', 'Restaurante Kilo', 'McDonald\'s', 'Subway'],
    'Transporte': ['Uber', '99', 'Posto Shell', 'Estacionamento', 'Metrô', 'Pedágio'],
    'Lazer': ['Netflix', 'Spotify', 'Cinema', 'Bar do João', 'Festa', 'Shopping'],
    'Educação': ['Livraria Cultura', 'Curso Online', 'Material Escolar', 'Udemy'],
    'Saúde': ['Farmácia', 'Academia', 'Consulta Médica', 'Plano de Saúde'],
    'Contas': ['Energia Elétrica', 'Água', 'Internet', 'Celular', 'Aluguel'],
}

INCOME_SOURCES = ['Salário', 'Freelance', 'Mesada', 'Venda', 'Rendimento']


def get_user_by_email(email: str):
    """Get user UID by email"""
    try:
        user = firebase_auth.get_user_by_email(email)
        return user.uid
    except Exception as e:
        print(f"Error getting user: {e}")
        return None


def generate_transactions(user_id: str, num_days: int = 30):
    """Generate synthetic transactions for the past N days"""
    db = get_firestore_client()
    transactions = []

    # Generate transactions for the past num_days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=num_days)

    current_date = start_date

    while current_date <= end_date:
        # Generate 1-5 transactions per day
        num_transactions = random.randint(1, 5)

        for _ in range(num_transactions):
            # 70% expenses, 30% income
            is_expense = random.random() < 0.7

            if is_expense:
                # Generate expense
                category = random.choice(list(CATEGORIES.keys()))
                merchant = random.choice(CATEGORIES[category])

                # Amount varies by category
                if category == 'Alimentação':
                    amount = round(random.uniform(10, 150), 2)
                elif category == 'Transporte':
                    amount = round(random.uniform(5, 80), 2)
                elif category == 'Lazer':
                    amount = round(random.uniform(20, 200), 2)
                elif category == 'Educação':
                    amount = round(random.uniform(30, 300), 2)
                elif category == 'Saúde':
                    amount = round(random.uniform(20, 400), 2)
                elif category == 'Contas':
                    amount = round(random.uniform(50, 500), 2)
                else:
                    amount = round(random.uniform(10, 100), 2)

                transaction = {
                    'user_id': user_id,
                    'type': 'expense',
                    'category': category,
                    'amount': amount,
                    'description': merchant,
                    'date': current_date.replace(
                        hour=random.randint(8, 22),
                        minute=random.randint(0, 59)
                    ),
                    'created_at': datetime.now(),
                }
            else:
                # Generate income
                source = random.choice(INCOME_SOURCES)
                amount = round(random.uniform(100, 2000), 2)

                transaction = {
                    'user_id': user_id,
                    'type': 'income',
                    'category': 'Receita',
                    'amount': amount,
                    'description': source,
                    'date': current_date.replace(
                        hour=random.randint(8, 18),
                        minute=random.randint(0, 59)
                    ),
                    'created_at': datetime.now(),
                }

            transactions.append(transaction)

        current_date += timedelta(days=1)

    # Save to Firestore
    print(f"Creating {len(transactions)} transactions...")

    for i, transaction in enumerate(transactions):
        # Generate a unique ID for the transaction
        doc_ref = db.collection('transactions').document()
        transaction['id'] = doc_ref.id
        doc_ref.set(transaction)
        if (i + 1) % 10 == 0:
            print(f"  Created {i + 1}/{len(transactions)} transactions...")

    print(f"✅ Successfully created {len(transactions)} transactions!")

    # Calculate and display summary
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    balance = total_income - total_expenses

    print(f"\n📊 Summary:")
    print(f"  Total Income:   R$ {total_income:,.2f}")
    print(f"  Total Expenses: R$ {total_expenses:,.2f}")
    print(f"  Balance:        R$ {balance:,.2f}")

    # Category breakdown
    print(f"\n📈 Expenses by Category:")
    category_totals = {}
    for t in transactions:
        if t['type'] == 'expense':
            category = t['category']
            category_totals[category] = category_totals.get(category, 0) + t['amount']

    for category, total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        percentage = (total / total_expenses) * 100 if total_expenses > 0 else 0
        print(f"  {category:15s}: R$ {total:7,.2f} ({percentage:5.1f}%)")


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

    # Generate transactions for the past 30 days
    print(f"\n📝 Generating synthetic transactions...")
    generate_transactions(user_id, num_days=30)

    print(f"\n✨ Done! You can now view the transactions in the app.")


if __name__ == "__main__":
    main()
