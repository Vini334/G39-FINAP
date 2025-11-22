"""
Analytics API Routes
Endpoints for analytics and spending breakdowns.
"""

from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from services.analytics_service import AnalyticsService
from schemas.transaction import (
    SpendingBreakdownResponse,
    RecentTransactionsResponse,
    SpendingTrendsResponse,
    CategoryStatsResponse
)
from schemas.common import APIResponse

router = APIRouter()
analytics_service = AnalyticsService()


@router.get("/spending-breakdown", response_model=APIResponse)
async def get_spending_breakdown(
    user_id: str = Query(..., description="User ID"),
    time_range: str = Query("month", description="Time range: month, 6months, or year")
):
    """
    Get spending breakdown by category for a time range.

    **Query Parameters:**
    - user_id: User ID (required)
    - time_range: "month", "6months", or "year" (default: "month")

    **Returns:**
    - Spending breakdown with categories, amounts, percentages, and colors
    """
    try:
        breakdown = analytics_service.get_spending_breakdown(user_id, time_range)

        response = SpendingBreakdownResponse(**breakdown)

        return APIResponse(
            success=True,
            data=response.dict(),
            message=f"Spending breakdown for {breakdown['period_label']} retrieved successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/transactions/recent", response_model=APIResponse)
async def get_recent_transactions(
    user_id: str = Query(..., description="User ID"),
    limit: int = Query(10, ge=1, le=100, description="Number of transactions to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    type: Optional[str] = Query(None, description="Filter by type: income or expense"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    """
    Get recent transactions with pagination and filters.

    **Query Parameters:**
    - user_id: User ID (required)
    - limit: Number of transactions (1-100, default: 10)
    - offset: Offset for pagination (default: 0)
    - type: Filter by type (income/expense, optional)
    - category: Filter by category (optional)

    **Returns:**
    - List of recent transactions with pagination info
    """
    try:
        result = analytics_service.get_recent_transactions(
            user_id=user_id,
            limit=limit,
            offset=offset,
            transaction_type=type,
            category=category
        )

        response = RecentTransactionsResponse(**result)

        return APIResponse(
            success=True,
            data=response.dict(),
            message=f"Retrieved {len(result['transactions'])} transactions"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/spending-trends", response_model=APIResponse)
async def get_spending_trends(
    user_id: str = Query(..., description="User ID"),
    months: int = Query(6, ge=1, le=24, description="Number of months to analyze")
):
    """
    Get spending trends over time.

    **Query Parameters:**
    - user_id: User ID (required)
    - months: Number of months to analyze (1-24, default: 6)

    **Returns:**
    - Monthly trends with income, expenses, and balance
    """
    try:
        trends = analytics_service.get_spending_trends(user_id, months)

        response = SpendingTrendsResponse(**trends)

        return APIResponse(
            success=True,
            data=response.dict(),
            message=f"Spending trends for {months} months retrieved successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/category-stats", response_model=APIResponse)
async def get_category_stats(
    user_id: str = Query(..., description="User ID"),
    category: str = Query(..., description="Category name"),
    time_range: str = Query("month", description="Time range: month, 6months, or year")
):
    """
    Get detailed statistics for a specific category.

    **Query Parameters:**
    - user_id: User ID (required)
    - category: Category name (required)
    - time_range: "month", "6months", or "year" (default: "month")

    **Returns:**
    - Detailed stats for the category (total, count, average, max, min)
    """
    try:
        stats = analytics_service.get_category_stats(user_id, category, time_range)

        response = CategoryStatsResponse(**stats)

        return APIResponse(
            success=True,
            data=response.dict(),
            message=f"Category stats for '{category}' retrieved successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
