"""
Script to setup Firebase Firestore collections and create test data.
Run this script to initialize the database with required collections.
"""

import sys
import os
from datetime import datetime

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import init_firebase, get_firestore_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def setup_collections():
    """Setup Firebase collections and create test data"""

    print("🔧 Initializing Firebase...")
    init_firebase()
    db = get_firestore_client()

    print("✅ Firebase initialized successfully\n")

    # Check existing collections
    print("📋 Checking existing collections...")
    collections = db.collections()
    existing_collections = [col.id for col in collections]
    print(f"Found collections: {existing_collections}\n")

    # Create test user
    print("👤 Creating test user...")
    users_ref = db.collection('users')

    # Check if test user already exists
    test_user_id = 'test-user-whatsapp'
    test_user_ref = users_ref.document(test_user_id)

    if test_user_ref.get().exists:
        print(f"⚠️  Test user already exists with ID: {test_user_id}")
        print("Do you want to update it? (y/n): ", end='')
        response = input().lower()
        if response != 'y':
            print("Skipping user creation...")
        else:
            update_test_user(test_user_ref)
    else:
        create_test_user(test_user_ref)

    # Setup system collections
    print("\n📚 Setting up system collections...")
    setup_system_collections(db)

    print("\n✅ Firebase setup complete!")
    print(f"\n📝 Test user ID: {test_user_id}")
    print("You can now test WhatsApp integration with this user.")


def create_test_user(user_ref):
    """Create a new test user"""

    print("\n📱 Enter your phone number (with country code, e.g., +5511999999999):")
    phone = input("> ").strip()

    if not phone.startswith('+'):
        print("⚠️  Phone number should start with + and country code")
        phone = '+' + phone

    user_data = {
        'uid': user_ref.id,
        'email': 'test@finap.com',
        'name': 'Teste WhatsApp',
        'phone': phone,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'is_active': True,
        'is_premium': False,
        'profile': {
            'age': 25,
            'monthly_income': 3000.0,
            'financial_goals': ['emergency_fund', 'travel'],
            'avatar_url': None
        },
        'gamification': {
            'level': 1,
            'xp': 0,
            'coins': 100,
            'lives': 5,
            'badges': [],
            'current_streak': 0,
            'longest_streak': 0,
            'last_login': datetime.now().isoformat()
        },
        'preferences': {
            'notifications': True,
            'dark_mode': False,
            'language': 'pt-BR',
            'currency': 'BRL'
        }
    }

    user_ref.set(user_data)
    print(f"✅ Test user created with phone: {phone}")
    print(f"   Email: test@finap.com")
    print(f"   User ID: {user_ref.id}")


def update_test_user(user_ref):
    """Update existing test user"""

    print("\n📱 Enter your phone number (with country code, e.g., +5511999999999):")
    phone = input("> ").strip()

    if not phone.startswith('+'):
        phone = '+' + phone

    user_ref.update({
        'phone': phone,
        'updated_at': datetime.now().isoformat()
    })

    print(f"✅ Test user updated with phone: {phone}")


def setup_system_collections(db):
    """Setup system collections with initial data"""

    # Categories
    print("📁 Setting up categories...")
    categories_ref = db.collection('system').document('categories')

    categories_data = {
        'categories': [
            {
                'id': 'alimentacao',
                'name': 'Alimentação',
                'icon': '🍔',
                'color': '#FF6B6B',
                'keywords': ['mercado', 'supermercado', 'restaurante', 'lanche', 'ifood']
            },
            {
                'id': 'transporte',
                'name': 'Transporte',
                'icon': '🚗',
                'color': '#4ECDC4',
                'keywords': ['uber', '99', 'taxi', 'gasolina', 'combustivel']
            },
            {
                'id': 'moradia',
                'name': 'Moradia',
                'icon': '🏠',
                'color': '#95E1D3',
                'keywords': ['aluguel', 'luz', 'agua', 'internet', 'gas']
            },
            {
                'id': 'lazer',
                'name': 'Lazer',
                'icon': '🎮',
                'color': '#F38181',
                'keywords': ['cinema', 'netflix', 'spotify', 'bar', 'festa']
            },
            {
                'id': 'saude',
                'name': 'Saúde',
                'icon': '⚕️',
                'color': '#AA96DA',
                'keywords': ['farmacia', 'medico', 'consulta', 'exame']
            },
            {
                'id': 'educacao',
                'name': 'Educação',
                'icon': '📚',
                'color': '#FCBAD3',
                'keywords': ['curso', 'faculdade', 'livro', 'material']
            },
            {
                'id': 'compras',
                'name': 'Compras',
                'icon': '🛍️',
                'color': '#A8D8EA',
                'keywords': ['roupa', 'sapato', 'presente', 'shopping']
            },
            {
                'id': 'outros',
                'name': 'Outros',
                'icon': '📦',
                'color': '#DFE6E9',
                'keywords': []
            }
        ],
        'updated_at': datetime.now().isoformat()
    }

    categories_ref.set(categories_data)
    print("✅ Categories created")

    # Config
    print("⚙️  Setting up config...")
    config_ref = db.collection('system').document('config')

    config_data = {
        'app_version': '1.0.0',
        'min_supported_version': '1.0.0',
        'maintenance_mode': False,
        'features': {
            'whatsapp_enabled': True,
            'fim_enabled': True,
            'gamification_enabled': True,
            'squads_enabled': False
        },
        'updated_at': datetime.now().isoformat()
    }

    config_ref.set(config_data)
    print("✅ Config created")


def list_collections():
    """List all collections in Firestore"""

    print("🔧 Initializing Firebase...")
    init_firebase()
    db = get_firestore_client()

    print("\n📋 Existing collections:")
    collections = db.collections()

    for collection in collections:
        print(f"\n📁 {collection.id}")

        # Count documents
        docs = collection.limit(5).stream()
        doc_count = 0
        for doc in docs:
            doc_count += 1
            print(f"   └─ {doc.id}")

        if doc_count == 5:
            print(f"   └─ ... (showing first 5)")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Setup Firebase Firestore collections')
    parser.add_argument('--list', action='store_true', help='List existing collections')
    parser.add_argument('--setup', action='store_true', help='Setup collections and test data')

    args = parser.parse_args()

    if args.list:
        list_collections()
    elif args.setup:
        setup_collections()
    else:
        print("Usage:")
        print("  python setup_firebase_collections.py --list     # List collections")
        print("  python setup_firebase_collections.py --setup    # Setup collections")
