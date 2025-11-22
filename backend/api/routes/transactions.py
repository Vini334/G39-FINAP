"""
Transaction Routes
API endpoints for transaction management.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime
from models.transaction import TransactionType
from schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionListResponse
)
from schemas.common import SuccessResponse
from services.transaction_service import TransactionService
from utils.categories import get_all_categories

router = APIRouter()
transaction_service = TransactionService()


# Temporary: Mock user ID for MVP (replace with auth later)
MOCK_USER_ID = "test-user-123"


@router.post("", response_model=SuccessResponse, status_code=201)
async def create_transaction(transaction_data: TransactionCreate):
    """
    Create a new transaction.

    **Request Body:**
    - type: Transaction type (income or expense)
    - amount: Amount (must be positive)
    - category: Category name
    - description: Optional description
    - date: Transaction date (default: now)
    - tags: Optional tags
    - is_recurrent: Is this a recurring transaction?
    - recurrence_period: Recurrence period if applicable

    **Returns:**
    - Created transaction with generated ID
    """
    try:
        transaction = await transaction_service.create_transaction(
            transaction_data=transaction_data,
            user_id=MOCK_USER_ID
        )

        return SuccessResponse(
            success=True,
            data={
                "transaction": TransactionResponse(**transaction.dict()),
                "message": "Transaction created successfully"
            },
            message="Transaction created successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=SuccessResponse)
async def list_transactions(
    limit: int = Query(20, ge=1, le=100, description="Number of transactions to return"),
    offset: int = Query(0, ge=0, description="Number of transactions to skip"),
    type: Optional[TransactionType] = Query(None, description="Filter by type (income/expense)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date")
):
    """
    List user transactions with optional filters.

    **Query Parameters:**
    - limit: Maximum number of results (1-100, default: 20)
    - offset: Number of results to skip (for pagination)
    - type: Filter by transaction type
    - category: Filter by category name
    - start_date: Filter transactions after this date
    - end_date: Filter transactions before this date

    **Returns:**
    - List of transactions
    - Total count
    - Pagination info
    """
    try:
        transactions = await transaction_service.get_transactions(
            user_id=MOCK_USER_ID,
            limit=limit,
            offset=offset,
            type_filter=type,
            category=category,
            start_date=start_date,
            end_date=end_date
        )

        # Get total count (simplified for MVP)
        total = len(transactions)

        # Convert to response format
        transaction_responses = [
            TransactionResponse(**t.dict()) for t in transactions
        ]

        return SuccessResponse(
            success=True,
            data={
                "transactions": transaction_responses,
                "total": total,
                "page": offset // limit + 1,
                "limit": limit,
                "total_pages": (total + limit - 1) // limit
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{transaction_id}", response_model=SuccessResponse)
async def get_transaction(transaction_id: str):
    """
    Get a single transaction by ID.

    **Path Parameters:**
    - transaction_id: Transaction ID

    **Returns:**
    - Transaction details
    """
    try:
        transaction = await transaction_service.get_transaction(
            transaction_id=transaction_id,
            user_id=MOCK_USER_ID
        )

        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        return SuccessResponse(
            success=True,
            data={"transaction": TransactionResponse(**transaction.dict())}
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{transaction_id}", response_model=SuccessResponse)
async def update_transaction(transaction_id: str, update_data: TransactionUpdate):
    """
    Update a transaction.

    **Path Parameters:**
    - transaction_id: Transaction ID

    **Request Body:**
    - Fields to update (all optional)

    **Returns:**
    - Updated transaction
    """
    try:
        transaction = await transaction_service.update_transaction(
            transaction_id=transaction_id,
            user_id=MOCK_USER_ID,
            update_data=update_data
        )

        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        return SuccessResponse(
            success=True,
            data={
                "transaction": TransactionResponse(**transaction.dict()),
                "message": "Transaction updated successfully"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{transaction_id}", response_model=SuccessResponse)
async def delete_transaction(transaction_id: str):
    """
    Delete a transaction.

    **Path Parameters:**
    - transaction_id: Transaction ID

    **Returns:**
    - Success message
    """
    try:
        deleted = await transaction_service.delete_transaction(
            transaction_id=transaction_id,
            user_id=MOCK_USER_ID
        )

        if not deleted:
            raise HTTPException(status_code=404, detail="Transaction not found")

        return SuccessResponse(
            success=True,
            data={},
            message="Transaction deleted successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories/list", response_model=SuccessResponse)
async def list_categories():
    """
    Get all available transaction categories.

    **Returns:**
    - List of categories with metadata (id, name, icon, color)
    """
    try:
        categories = get_all_categories()

        return SuccessResponse(
            success=True,
            data={"categories": categories}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
