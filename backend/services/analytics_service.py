"""
Analytics Service
Business logic for analytics and spending breakdowns.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from core.database import get_firestore_client
from collections import defaultdict


# Category colors (matching Google AI design)
CATEGORY_COLORS = {
    "alimentacao": "#10B981",      # Green
    "transporte": "#3B82F6",       # Blue
    "moradia": "#8B5CF6",          # Purple
    "saude": "#EF4444",            # Red
    "educacao": "#F59E0B",         # Amber
    "lazer": "#EC4899",            # Pink
    "compras": "#14B8A6",          # Teal
    "outros": "#6B7280",           # Gray
}


class AnalyticsService:
    """Service for analytics and spending breakdowns"""

    def __init__(self):
        self.db = get_firestore_client()

    def get_spending_breakdown(
        self,
        user_id: str,
        time_range: str = "month"
    ) -> Dict:
        """
        Get spending breakdown by category for a time range.

        Args:
            user_id: User ID
            time_range: "month", "6months", or "year"

        Returns:
            Dictionary with categories breakdown and time range info
        """
        # Calculate date range
        end_date = datetime.now()

        if time_range == "month":
            start_date = datetime(end_date.year, end_date.month, 1)
            period_label = "Este Mês"
        elif time_range == "6months":
            start_date = end_date - timedelta(days=180)
            period_label = "Últimos 6 Meses"
        elif time_range == "year":
            start_date = end_date - timedelta(days=365)
            period_label = "Último Ano"
        else:
            start_date = datetime(end_date.year, end_date.month, 1)
            period_label = "Este Mês"

        # Get transactions
        transactions_ref = self.db.collection('transactions') \
            .where('user_id', '==', user_id) \
            .where('type', '==', 'expense') \
            .where('date', '>=', start_date) \
            .where('date', '<=', end_date)

        transactions = list(transactions_ref.stream())

        # Aggregate by category
        category_totals = defaultdict(float)
        total_expenses = 0.0

        for doc in transactions:
            data = doc.to_dict()
            category = data.get('category', 'outros').lower()
            amount = float(data.get('amount', 0))

            category_totals[category] += amount
            total_expenses += amount

        # Build category breakdown
        categories = []
        for category, amount in category_totals.items():
            percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0

            categories.append({
                "name": category.capitalize(),
                "amount": round(amount, 2),
                "percentage": round(percentage, 1),
                "color": CATEGORY_COLORS.get(category, CATEGORY_COLORS["outros"])
            })

        # Sort by amount (descending)
        categories.sort(key=lambda x: x['amount'], reverse=True)

        return {
            "time_range": time_range,
            "period_label": period_label,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_expenses": round(total_expenses, 2),
            "categories": categories,
            "transaction_count": len(transactions)
        }

    def get_recent_transactions(
        self,
        user_id: str,
        limit: int = 10,
        offset: int = 0,
        transaction_type: Optional[str] = None,
        category: Optional[str] = None
    ) -> Dict:
        """
        Get recent transactions with pagination and filters.

        Args:
            user_id: User ID
            limit: Number of transactions to return
            offset: Offset for pagination
            transaction_type: Filter by type ("income" or "expense")
            category: Filter by category

        Returns:
            Dictionary with transactions list and pagination info
        """
        # Build query
        query = self.db.collection('transactions').where('user_id', '==', user_id)

        if transaction_type:
            query = query.where('type', '==', transaction_type)

        if category:
            query = query.where('category', '==', category)

        # Order by date (most recent first)
        query = query.order_by('date', direction='DESCENDING')

        # Get transactions
        all_docs = list(query.stream())
        total_count = len(all_docs)

        # Apply pagination
        paginated_docs = all_docs[offset:offset + limit]

        # Build transactions list
        transactions = []
        for doc in paginated_docs:
            data = doc.to_dict()

            # Convert date to string if it's a datetime
            date = data.get('date')
            if isinstance(date, datetime):
                date_str = date.isoformat()
            else:
                date_str = str(date)

            transactions.append({
                "id": doc.id,
                "type": data.get('type'),
                "amount": float(data.get('amount', 0)),
                "category": data.get('category', 'outros'),
                "description": data.get('description', ''),
                "date": date_str,
                "source": data.get('source', 'app'),
                "created_at": data.get('created_at', datetime.now()).isoformat() if isinstance(data.get('created_at'), datetime) else str(data.get('created_at', ''))
            })

        return {
            "transactions": transactions,
            "total": total_count,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total_count
        }

    def get_spending_trends(
        self,
        user_id: str,
        months: int = 6
    ) -> Dict:
        """
        Get spending trends over time.

        Args:
            user_id: User ID
            months: Number of months to analyze

        Returns:
            Dictionary with monthly spending data
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)

        # Get transactions
        transactions_ref = self.db.collection('transactions') \
            .where('user_id', '==', user_id) \
            .where('date', '>=', start_date) \
            .where('date', '<=', end_date)

        transactions = list(transactions_ref.stream())

        # Aggregate by month
        monthly_data = defaultdict(lambda: {"income": 0.0, "expenses": 0.0})

        for doc in transactions:
            data = doc.to_dict()
            date = data.get('date')

            if isinstance(date, datetime):
                month_key = date.strftime('%Y-%m')
            else:
                month_key = str(date)[:7]  # Extract YYYY-MM

            amount = float(data.get('amount', 0))
            trans_type = data.get('type')

            if trans_type == 'income':
                monthly_data[month_key]["income"] += amount
            elif trans_type == 'expense':
                monthly_data[month_key]["expenses"] += amount

        # Build monthly trends
        trends = []
        for month_key in sorted(monthly_data.keys()):
            data = monthly_data[month_key]
            trends.append({
                "month": month_key,
                "income": round(data["income"], 2),
                "expenses": round(data["expenses"], 2),
                "balance": round(data["income"] - data["expenses"], 2)
            })

        return {
            "months": months,
            "trends": trends
        }

    def get_category_stats(
        self,
        user_id: str,
        category: str,
        time_range: str = "month"
    ) -> Dict:
        """
        Get detailed stats for a specific category.

        Args:
            user_id: User ID
            category: Category name
            time_range: "month", "6months", or "year"

        Returns:
            Dictionary with category statistics
        """
        # Calculate date range
        end_date = datetime.now()

        if time_range == "month":
            start_date = datetime(end_date.year, end_date.month, 1)
        elif time_range == "6months":
            start_date = end_date - timedelta(days=180)
        elif time_range == "year":
            start_date = end_date - timedelta(days=365)
        else:
            start_date = datetime(end_date.year, end_date.month, 1)

        # Get category transactions
        transactions_ref = self.db.collection('transactions') \
            .where('user_id', '==', user_id) \
            .where('type', '==', 'expense') \
            .where('category', '==', category.lower()) \
            .where('date', '>=', start_date) \
            .where('date', '<=', end_date)

        transactions = list(transactions_ref.stream())

        # Calculate stats
        total = 0.0
        count = len(transactions)
        amounts = []

        for doc in transactions:
            data = doc.to_dict()
            amount = float(data.get('amount', 0))
            total += amount
            amounts.append(amount)

        average = total / count if count > 0 else 0
        max_amount = max(amounts) if amounts else 0
        min_amount = min(amounts) if amounts else 0

        return {
            "category": category,
            "time_range": time_range,
            "total": round(total, 2),
            "count": count,
            "average": round(average, 2),
            "max": round(max_amount, 2),
            "min": round(min_amount, 2),
            "color": CATEGORY_COLORS.get(category.lower(), CATEGORY_COLORS["outros"])
        }
