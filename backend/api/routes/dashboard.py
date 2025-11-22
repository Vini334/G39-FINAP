"""
Dashboard Routes
API endpoints for dashboard data and summaries.
"""

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from schemas.transaction import DashboardSummary, TransactionResponse
from schemas.common import SuccessResponse, APIResponse
from schemas.gamification import DashboardSummaryResponse, DashboardStats, BalanceInfo, BudgetAlertInfo, MissionResponse
from services.transaction_service import TransactionService
from services.gamification_service import GamificationService
from services.mission_service import MissionService
from core.database import get_firestore_client
from models.gamification import MissionStatus

router = APIRouter()
transaction_service = TransactionService()
gamification_service = GamificationService()
mission_service = MissionService()

# Temporary: Mock user ID for MVP (replace with auth later)
MOCK_USER_ID = "test-user-123"


@router.get("/summary", response_model=SuccessResponse)
async def get_dashboard_summary(
    start_date: datetime = Query(None, description="Start date for summary period"),
    end_date: datetime = Query(None, description="End date for summary period")
):
    """
    Get dashboard summary with financial overview.

    **Query Parameters:**
    - start_date: Start date (default: first day of current month)
    - end_date: End date (default: now)

    **Returns:**
    - Dashboard summary with:
      - Total income
      - Total expenses
      - Balance
      - Savings rate
      - Top categories breakdown
      - Transaction count
    """
    try:
        # Get summary data
        summary = await transaction_service.get_summary(
            user_id=MOCK_USER_ID,
            start_date=start_date,
            end_date=end_date
        )

        # Get recent transactions for the period
        recent_transactions = await transaction_service.get_transactions(
            user_id=MOCK_USER_ID,
            start_date=start_date,
            end_date=end_date,
            limit=5  # Last 5 transactions
        )

        # Build dashboard response
        dashboard = DashboardSummary(
            period=f"{summary['period']['start'][:10]} to {summary['period']['end'][:10]}",
            total_income=summary['total_income'],
            total_expenses=summary['total_expenses'],
            balance=summary['balance'],
            savings_rate=summary['savings_rate'],
            categories=summary['categories'],
            transaction_count=summary['transaction_count'],
            recent_transactions=[
                TransactionResponse(**t.dict()) for t in recent_transactions
            ]
        )

        return SuccessResponse(
            success=True,
            data=dashboard.dict()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=SuccessResponse)
async def get_dashboard_stats():
    """
    Get additional dashboard statistics.

    **Returns:**
    - Extended statistics for dashboard cards
    """
    try:
        # Get current month summary
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)

        summary = await transaction_service.get_summary(
            user_id=MOCK_USER_ID,
            start_date=start_of_month,
            end_date=now
        )

        # Additional stats
        stats = {
            "current_month": {
                "income": summary['total_income'],
                "expenses": summary['total_expenses'],
                "balance": summary['balance'],
                "savings_rate": summary['savings_rate']
            },
            "quick_stats": {
                "transactions_this_month": summary['transaction_count'],
                "days_in_month": now.day,
                "daily_average": round(
                    summary['total_expenses'] / now.day, 2
                ) if now.day > 0 else 0,
                "top_category": summary['categories'][0].category if summary['categories'] else "N/A"
            }
        }

        return SuccessResponse(
            success=True,
            data=stats
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/overview/{user_id}", response_model=APIResponse)
async def get_dashboard_overview(user_id: str):
    """
    Get complete dashboard overview for a user.

    This endpoint combines:
    - Gamification stats (level, XP, lives, streak, coins)
    - Balance information
    - Budget alerts
    - Daily missions
    - Learning progress (optional)

    **Returns:**
    - Complete dashboard data for the Overview screen
    """
    try:
        db = get_firestore_client()

        # Get user document
        user_doc = db.collection('users').document(user_id).get()

        if not user_doc.exists:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")

        user_data = user_doc.to_dict()
        gamification = user_data.get('gamification', {})
        profile = user_data.get('profile', {})

        # 1. Gamification stats
        total_xp = gamification.get('xp', 0)
        current_level = gamification.get('level', 1)
        current_lives = gamification.get('lives', 5)
        current_streak = gamification.get('current_streak', 0)
        current_coins = gamification.get('coins', 100)

        # Calculate level info
        level_data = gamification_service.get_level_info(total_xp)
        xp_to_next = gamification_service.calculate_xp_to_next_level(total_xp, current_level)
        progress_pct = gamification_service.calculate_progress_percentage(total_xp, current_level)

        # Next level XP
        next_level_xp = level_data.max_xp if level_data.max_xp else total_xp + 100

        stats = DashboardStats(
            lives=current_lives,
            max_lives=5,
            streak=current_streak,
            coins=current_coins,
            level=current_level,
            current_xp=total_xp,
            next_level_xp=next_level_xp,
            xp_percentage=progress_pct
        )

        # 2. Balance information
        # Get transactions for current month
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)

        summary = await transaction_service.get_summary(
            user_id=user_id,
            start_date=start_of_month,
            end_date=now
        )

        monthly_budget = profile.get('monthly_budget', 3000.0)  # Default R$3000
        spent_this_month = summary['total_expenses']
        budget_percentage = int((spent_this_month / monthly_budget) * 100) if monthly_budget > 0 else 0

        balance = BalanceInfo(
            current=summary['balance'],
            spent_this_month=spent_this_month,
            monthly_budget=monthly_budget,
            budget_percentage=budget_percentage
        )

        # 3. Budget alert
        show_alert = budget_percentage >= 80
        alert_message = ""

        if budget_percentage >= 100:
            alert_message = f"Você ultrapassou seu orçamento! {budget_percentage}% gasto."
        elif budget_percentage >= 80:
            alert_message = f"Atenção! Você já gastou {budget_percentage}% do seu orçamento mensal."

        budget_alert = BudgetAlertInfo(
            show=show_alert,
            percentage=budget_percentage,
            message=alert_message
        )

        # 4. Daily missions
        mission_service.expire_old_missions(user_id)
        missions = mission_service.get_daily_missions(user_id)

        missions_response = []
        for mission in missions:
            missions_response.append(MissionResponse(
                id=mission.id,
                type=mission.type.value,
                title=mission.title,
                description=mission.description,
                xp_reward=mission.xp_reward,
                coins_reward=mission.coins_reward,
                status=mission.status.value,
                progress=mission.progress,
                target=mission.target,
                completed=mission.status == MissionStatus.COMPLETED,
                date=mission.date
            ))

        # 5. Learning progress (optional - to be implemented later)
        learning_progress = None

        # Build response
        dashboard_response = DashboardSummaryResponse(
            stats=stats,
            balance=balance,
            budget_alert=budget_alert,
            missions=missions_response,
            learning_progress=learning_progress
        )

        return APIResponse(
            success=True,
            data=dashboard_response.dict(),
            message="Dashboard overview retrieved successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
