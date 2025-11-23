"""
Transaction Service
Business logic for transaction management.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict
from models.transaction import Transaction, TransactionType, TransactionSource
from schemas.transaction import TransactionCreate, TransactionUpdate, CategorySummary
from core.database import get_firestore_client
from firebase_admin import firestore
from utils.categories import categorize_transaction
import uuid


class TransactionService:
    """Service for managing transactions"""

    def __init__(self):
        self.db = None

    def _get_db(self):
        """Get Firestore client (lazy initialization)"""
        if self.db is None:
            try:
                self.db = get_firestore_client()
            except RuntimeError:
                # Firebase not configured, use mock mode
                self.db = None
        return self.db

    async def create_transaction(
        self,
        transaction_data: TransactionCreate,
        user_id: str
    ) -> Transaction:
        """
        Create a new transaction.

        Args:
            transaction_data: Transaction creation data
            user_id: User ID who created the transaction

        Returns:
            Created transaction
        """
        # Auto-categorize if category is empty or "outros"
        category = transaction_data.category
        if category == "outros" or not category:
            if transaction_data.description:
                category = categorize_transaction(transaction_data.description)
            else:
                category = "outros"

        # Create transaction object
        transaction = Transaction(
            id=str(uuid.uuid4()),
            user_id=user_id,
            type=transaction_data.type,
            amount=transaction_data.amount,
            category=category,
            description=transaction_data.description,
            date=transaction_data.date or datetime.now(),
            source=TransactionSource.APP,
            tags=transaction_data.tags,
            is_recurrent=transaction_data.is_recurrent,
            recurrence_period=transaction_data.recurrence_period,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Save to Firestore
        db = self._get_db()
        if db:
            doc_ref = db.collection('transactions').document(transaction.id)
            doc_ref.set(transaction.dict())

        return transaction

    async def get_transactions(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0,
        type_filter: Optional[TransactionType] = None,
        category: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Transaction]:
        """
        Get user transactions with filters.

        Args:
            user_id: User ID
            limit: Maximum number of transactions to return
            offset: Number of transactions to skip
            type_filter: Filter by transaction type
            category: Filter by category
            start_date: Filter by start date
            end_date: Filter by end date

        Returns:
            List of transactions
        """
        db = self._get_db()
        transactions = []

        if db:
            try:
                # Simple query - just filter by user_id to avoid composite index requirement
                query = db.collection('transactions').where('user_id', '==', user_id)

                # Execute query and get all transactions
                print(f"DEBUG - Querying transactions for user_id={user_id}")
                docs = query.stream()

                all_transactions = []
                for doc in docs:
                    data = doc.to_dict()
                    try:
                        # Add document ID to data if not present
                        if 'id' not in data:
                            data['id'] = doc.id
                        all_transactions.append(Transaction(**data))
                    except Exception as e:
                        print(f"Warning: Failed to parse transaction {doc.id}: {e}")
                        continue

                # Filter in memory
                filtered_transactions = all_transactions

                if type_filter:
                    filtered_transactions = [t for t in filtered_transactions if t.type == type_filter]

                if category:
                    filtered_transactions = [t for t in filtered_transactions if t.category == category]

                if start_date:
                    # Convert transaction date to naive local time for comparison
                    # Firestore stores dates in UTC, so we need to convert to local timezone
                    filtered_transactions = [
                        t for t in filtered_transactions
                        if (t.date.astimezone().replace(tzinfo=None) if hasattr(t.date, 'astimezone') else t.date.replace(tzinfo=None))
                        >= start_date.replace(tzinfo=None)
                    ]

                if end_date:
                    # Convert transaction date to naive local time for comparison
                    # Firestore stores dates in UTC, so we need to convert to local timezone
                    filtered_transactions = [
                        t for t in filtered_transactions
                        if (t.date.astimezone().replace(tzinfo=None) if hasattr(t.date, 'astimezone') else t.date.replace(tzinfo=None))
                        <= end_date.replace(tzinfo=None)
                    ]

                # Sort by date descending
                filtered_transactions.sort(key=lambda x: x.date, reverse=True)

                # Apply pagination
                transactions = filtered_transactions[offset:offset + limit]

            except Exception as e:
                # Fallback to mock data if Firestore query fails
                print(f"Warning: Firestore query failed, using mock data: {e}")
                transactions = self._get_mock_transactions(user_id, limit)
        else:
            # Mock data for development
            transactions = self._get_mock_transactions(user_id, limit)

        return transactions

    async def get_transaction(self, transaction_id: str, user_id: str) -> Optional[Transaction]:
        """
        Get a single transaction by ID.

        Args:
            transaction_id: Transaction ID
            user_id: User ID (for authorization)

        Returns:
            Transaction or None if not found
        """
        db = self._get_db()

        if db:
            doc_ref = db.collection('transactions').document(transaction_id)
            doc = doc_ref.get()

            if doc.exists:
                data = doc.to_dict()
                if data['user_id'] == user_id:
                    # Add document ID to data if not present
                    if 'id' not in data:
                        data['id'] = doc.id
                    return Transaction(**data)

        return None

    async def update_transaction(
        self,
        transaction_id: str,
        user_id: str,
        update_data: TransactionUpdate
    ) -> Optional[Transaction]:
        """
        Update a transaction.

        Args:
            transaction_id: Transaction ID
            user_id: User ID (for authorization)
            update_data: Update data

        Returns:
            Updated transaction or None if not found
        """
        db = self._get_db()

        if db:
            doc_ref = db.collection('transactions').document(transaction_id)
            doc = doc_ref.get()

            if doc.exists:
                data = doc.to_dict()
                if data['user_id'] == user_id:
                    # Update fields
                    update_dict = update_data.dict(exclude_unset=True)
                    update_dict['updated_at'] = datetime.now()

                    doc_ref.update(update_dict)

                    # Get updated document
                    updated_doc = doc_ref.get()
                    updated_data = updated_doc.to_dict()
                    # Add document ID to data if not present
                    if 'id' not in updated_data:
                        updated_data['id'] = updated_doc.id
                    return Transaction(**updated_data)

        return None

    async def delete_transaction(self, transaction_id: str, user_id: str) -> bool:
        """
        Delete a transaction.

        Args:
            transaction_id: Transaction ID
            user_id: User ID (for authorization)

        Returns:
            True if deleted, False if not found
        """
        db = self._get_db()

        if db:
            doc_ref = db.collection('transactions').document(transaction_id)
            doc = doc_ref.get()

            if doc.exists:
                data = doc.to_dict()
                if data['user_id'] == user_id:
                    doc_ref.delete()
                    return True

        return False

    async def get_summary(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Get transaction summary for a period.

        Args:
            user_id: User ID
            start_date: Start date (default: start of current month)
            end_date: End date (default: now)

        Returns:
            Summary dictionary with totals and category breakdown
        """
        # Default to current month
        if not start_date:
            now = datetime.now()
            start_date = datetime(now.year, now.month, 1)

        if not end_date:
            end_date = datetime.now()

        print(f"DEBUG - get_summary called with start_date={start_date}, end_date={end_date}")

        try:
            # Get transactions for period
            transactions = await self.get_transactions(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
                limit=1000  # Get all transactions for period
            )
            print(f"DEBUG - Retrieved {len(transactions)} transactions for summary")
        except Exception as e:
            # Use mock transactions on error
            print(f"Warning: Failed to get transactions, using mock data: {e}")
            transactions = self._get_mock_transactions(user_id, 10)

        # Calculate totals
        total_income = sum(t.amount for t in transactions if t.type == TransactionType.INCOME)
        total_expenses = sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE)
        balance = total_income - total_expenses

        # Calculate savings rate
        savings_rate = (balance / total_income * 100) if total_income > 0 else 0

        # Category breakdown (expenses only)
        category_totals: Dict[str, float] = {}
        category_counts: Dict[str, int] = {}

        for transaction in transactions:
            if transaction.type == TransactionType.EXPENSE:
                cat = transaction.category
                category_totals[cat] = category_totals.get(cat, 0) + transaction.amount
                category_counts[cat] = category_counts.get(cat, 0) + 1

        # Build category summaries
        categories = []
        for cat, amount in category_totals.items():
            percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
            categories.append(
                CategorySummary(
                    category=cat,
                    amount=amount,
                    percentage=round(percentage, 2),
                    count=category_counts[cat]
                )
            )

        # Sort by amount (descending)
        categories.sort(key=lambda x: x.amount, reverse=True)

        return {
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "total_income": round(total_income, 2),
            "total_expenses": round(total_expenses, 2),
            "balance": round(balance, 2),
            "savings_rate": round(savings_rate, 2),
            "categories": categories[:5],  # Top 5 categories
            "transaction_count": len(transactions)
        }

    def _get_mock_transactions(self, user_id: str, limit: int) -> List[Transaction]:
        """Generate mock transactions for development"""
        mock_transactions = [
            Transaction(
                id="mock-1",
                user_id=user_id,
                type=TransactionType.EXPENSE,
                amount=45.50,
                category="alimentação",
                description="Almoço no restaurante",
                date=datetime.now() - timedelta(days=1),
                source=TransactionSource.APP,
                tags=["restaurante", "almoço"],
                is_recurrent=False
            ),
            Transaction(
                id="mock-2",
                user_id=user_id,
                type=TransactionType.EXPENSE,
                amount=30.00,
                category="transporte",
                description="Uber para o trabalho",
                date=datetime.now() - timedelta(days=2),
                source=TransactionSource.APP,
                tags=["uber", "trabalho"],
                is_recurrent=False
            ),
            Transaction(
                id="mock-3",
                user_id=user_id,
                type=TransactionType.INCOME,
                amount=3500.00,
                category="receita",
                description="Salário",
                date=datetime.now() - timedelta(days=5),
                source=TransactionSource.APP,
                tags=["salário"],
                is_recurrent=True,
                recurrence_period="monthly"
            ),
        ]

        return mock_transactions[:limit]
