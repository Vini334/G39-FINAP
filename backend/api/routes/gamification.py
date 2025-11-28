"""
Gamification API Routes
Endpoints for gamification features (XP, levels, lives, coins, challenges).
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict
from services.gamification_service import GamificationService
from services.mission_service import MissionService
from schemas.gamification import (
    AddXPRequest, SpendLivesRequest, AwardCoinsRequest,
    CreateChallengeRequest, UpdateChallengeProgressRequest,
    UpdateMissionProgressRequest,
    GamificationStats, XPTransactionResponse, LivesResponse,
    CoinsResponse, ChallengeResponse, ChallengesListResponse,
    LevelInfo, MissionResponse, CompleteMissionResponse, MissionProgressResponse
)
from schemas.common import APIResponse
from models.gamification import LEVELS, XP_REWARDS, XPAction, MissionStatus, MissionType
from core.database import get_firestore_client
from datetime import datetime, timedelta

router = APIRouter()
gamification_service = GamificationService()
mission_service = MissionService()


@router.get("/stats/{user_id}", response_model=APIResponse)
async def get_gamification_stats(user_id: str):
    """Get user's gamification statistics"""

    try:
        db = get_firestore_client()
        user_doc = db.collection('users').document(user_id).get()

        if not user_doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found"
            )

        user_data = user_doc.to_dict()
        gamification = user_data.get('gamification', {})

        # Get level info
        total_xp = gamification.get('xp', 0)
        current_level = gamification.get('level', 1)
        level_data = gamification_service.get_level_info(total_xp)

        xp_to_next = gamification_service.calculate_xp_to_next_level(total_xp, current_level)
        progress_pct = gamification_service.calculate_progress_percentage(total_xp, current_level)

        level_info = LevelInfo(
            level=current_level,
            title=level_data.title,
            min_xp=level_data.min_xp,
            max_xp=level_data.max_xp,
            current_xp=total_xp,
            xp_to_next_level=xp_to_next,
            progress_percentage=progress_pct
        )

        # Calculate next life recharge
        current_lives = gamification.get('lives', 5)
        max_lives = 5
        next_recharge = None

        if current_lives < max_lives:
            last_recharge = gamification.get('lives_last_recharge', datetime.now())
            if isinstance(last_recharge, str):
                last_recharge = datetime.fromisoformat(last_recharge.replace('Z', '+00:00'))
            next_recharge = last_recharge + timedelta(hours=5)

        stats = GamificationStats(
            user_id=user_id,
            level_info=level_info,
            total_xp=total_xp,
            coins=gamification.get('coins', 100),
            lives=current_lives,
            max_lives=max_lives,
            badges=gamification.get('badges', []),
            current_streak=gamification.get('current_streak', 0),
            longest_streak=gamification.get('longest_streak', 0),
            next_life_recharge=next_recharge
        )

        return APIResponse(
            success=True,
            data=stats.dict(),
            message="Gamification stats retrieved successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/xp/add", response_model=APIResponse)
async def add_xp(request: AddXPRequest):
    """Add XP to user for an action"""

    try:
        xp_added, level_up, new_level = gamification_service.add_xp(
            request.user_id,
            request.action,
            request.metadata
        )

        # Get updated stats
        db = get_firestore_client()
        user_doc = db.collection('users').document(request.user_id).get()
        user_data = user_doc.to_dict()
        gamification = user_data.get('gamification', {})

        total_xp = gamification.get('xp', 0)
        current_level = gamification.get('level', 1)
        level_data = gamification_service.get_level_info(total_xp)

        xp_to_next = gamification_service.calculate_xp_to_next_level(total_xp, current_level)
        progress_pct = gamification_service.calculate_progress_percentage(total_xp, current_level)

        level_info = LevelInfo(
            level=current_level,
            title=level_data.title,
            min_xp=level_data.min_xp,
            max_xp=level_data.max_xp,
            current_xp=total_xp,
            xp_to_next_level=xp_to_next,
            progress_percentage=progress_pct
        )

        message = f"Earned {xp_added} XP!"
        if level_up:
            message = f"🎉 Level Up! You're now level {new_level}! Earned {xp_added} XP."

        response = XPTransactionResponse(
            success=True,
            xp_added=xp_added,
            total_xp=total_xp,
            level_up=level_up,
            new_level=new_level,
            level_info=level_info,
            message=message
        )

        return APIResponse(
            success=True,
            data=response.dict(),
            message=message
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/lives/spend", response_model=APIResponse)
async def spend_lives(request: SpendLivesRequest):
    """Spend user lives"""

    try:
        remaining_lives, next_recharge = gamification_service.spend_lives(
            request.user_id,
            request.amount
        )

        recharge_time_remaining = 0
        if next_recharge:
            time_diff = next_recharge - datetime.now()
            recharge_time_remaining = int(time_diff.total_seconds() / 60)

        response = LivesResponse(
            success=True,
            current_lives=remaining_lives,
            max_lives=5,
            next_recharge=next_recharge,
            recharge_time_remaining_minutes=recharge_time_remaining,
            message=f"Spent {request.amount} life/lives. {remaining_lives} remaining."
        )

        return APIResponse(
            success=True,
            data=response.dict(),
            message=response.message
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/lives/recharge/{user_id}", response_model=APIResponse)
async def recharge_lives(user_id: str):
    """Recharge user lives based on time elapsed"""

    try:
        current_lives = gamification_service.recharge_lives(user_id)

        # Get next recharge time
        db = get_firestore_client()
        user_doc = db.collection('users').document(user_id).get()
        user_data = user_doc.to_dict()
        gamification = user_data.get('gamification', {})

        next_recharge = None
        recharge_time_remaining = 0

        if current_lives < 5:
            last_recharge = gamification.get('lives_last_recharge', datetime.now())
            if isinstance(last_recharge, str):
                last_recharge = datetime.fromisoformat(last_recharge.replace('Z', '+00:00'))
            next_recharge = last_recharge + timedelta(hours=5)
            time_diff = next_recharge - datetime.now()
            recharge_time_remaining = max(0, int(time_diff.total_seconds() / 60))

        response = LivesResponse(
            success=True,
            current_lives=current_lives,
            max_lives=5,
            next_recharge=next_recharge,
            recharge_time_remaining_minutes=recharge_time_remaining,
            message=f"Lives recharged. Current: {current_lives}/5"
        )

        return APIResponse(
            success=True,
            data=response.dict(),
            message=response.message
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/coins/award", response_model=APIResponse)
async def award_coins(request: AwardCoinsRequest):
    """Award coins to user"""

    try:
        total_coins = gamification_service.award_coins(
            request.user_id,
            request.amount,
            request.reason
        )

        response = CoinsResponse(
            success=True,
            coins_added=request.amount,
            total_coins=total_coins,
            message=f"Awarded {request.amount} coins! Total: {total_coins}"
        )

        return APIResponse(
            success=True,
            data=response.dict(),
            message=response.message
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/challenges", response_model=APIResponse)
async def create_challenge(request: CreateChallengeRequest):
    """Create a new challenge"""

    try:
        challenge = gamification_service.create_challenge(
            user_id=request.user_id,
            challenge_type=request.type,
            title=request.title,
            description=request.description,
            target=request.target,
            reward_xp=request.reward_xp,
            reward_coins=request.reward_coins,
            duration_days=request.duration_days
        )

        time_remaining = (challenge.expires_at - datetime.now()).total_seconds() / 3600

        response = ChallengeResponse(
            id=challenge.id,
            user_id=challenge.user_id,
            type=challenge.type.value,
            title=challenge.title,
            description=challenge.description,
            target=challenge.target,
            current=challenge.current,
            progress_percentage=int((challenge.current / challenge.target) * 100),
            reward_xp=challenge.reward_xp,
            reward_coins=challenge.reward_coins,
            status=challenge.status,
            starts_at=challenge.starts_at,
            expires_at=challenge.expires_at,
            time_remaining_hours=int(time_remaining)
        )

        return APIResponse(
            success=True,
            data=response.dict(),
            message="Challenge created successfully"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/challenges/{challenge_id}/progress", response_model=APIResponse)
async def update_challenge_progress(challenge_id: str, request: UpdateChallengeProgressRequest):
    """Update challenge progress"""

    try:
        challenge = gamification_service.update_challenge_progress(
            challenge_id,
            request.progress
        )

        time_remaining = None
        if challenge.status == "active":
            time_remaining = int((challenge.expires_at - datetime.now()).total_seconds() / 3600)

        response = ChallengeResponse(
            id=challenge.id,
            user_id=challenge.user_id,
            type=challenge.type.value,
            title=challenge.title,
            description=challenge.description,
            target=challenge.target,
            current=challenge.current,
            progress_percentage=int((challenge.current / challenge.target) * 100),
            reward_xp=challenge.reward_xp,
            reward_coins=challenge.reward_coins,
            status=challenge.status,
            starts_at=challenge.starts_at,
            expires_at=challenge.expires_at,
            completed_at=challenge.completed_at,
            time_remaining_hours=time_remaining
        )

        message = "Challenge updated"
        if challenge.status == "completed":
            message = f"🎉 Challenge completed! Earned {challenge.reward_xp} XP and {challenge.reward_coins} coins!"

        return APIResponse(
            success=True,
            data=response.dict(),
            message=message
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/challenges/{user_id}", response_model=APIResponse)
async def get_user_challenges(user_id: str):
    """Get all user challenges"""

    try:
        challenges_dict = gamification_service.get_user_challenges(user_id)

        def challenge_to_response(challenge):
            time_remaining = None
            if challenge.status == "active":
                time_remaining = int((challenge.expires_at - datetime.now()).total_seconds() / 3600)

            return ChallengeResponse(
                id=challenge.id,
                user_id=challenge.user_id,
                type=challenge.type.value,
                title=challenge.title,
                description=challenge.description,
                target=challenge.target,
                current=challenge.current,
                progress_percentage=int((challenge.current / challenge.target) * 100),
                reward_xp=challenge.reward_xp,
                reward_coins=challenge.reward_coins,
                status=challenge.status,
                starts_at=challenge.starts_at,
                expires_at=challenge.expires_at,
                completed_at=challenge.completed_at,
                time_remaining_hours=time_remaining
            )

        response = ChallengesListResponse(
            active_challenges=[challenge_to_response(c) for c in challenges_dict['active']],
            completed_challenges=[challenge_to_response(c) for c in challenges_dict['completed']],
            expired_challenges=[challenge_to_response(c) for c in challenges_dict['expired']]
        )

        return APIResponse(
            success=True,
            data=response.dict(),
            message=f"Found {len(challenges_dict['active'])} active challenges"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/streak/{user_id}", response_model=APIResponse)
async def update_streak(user_id: str):
    """Update user's login streak"""

    try:
        current_streak = gamification_service.update_streak(user_id)

        return APIResponse(
            success=True,
            data={"current_streak": current_streak},
            message=f"Streak updated! Current: {current_streak} days"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/xp-rewards", response_model=APIResponse)
async def get_xp_rewards():
    """Get list of all XP rewards"""

    rewards = []
    for action, reward in XP_REWARDS.items():
        rewards.append({
            "action": action.value,
            "amount": reward.amount,
            "description": reward.description
        })

    return APIResponse(
        success=True,
        data={"rewards": rewards},
        message="XP rewards retrieved successfully"
    )


@router.get("/levels", response_model=APIResponse)
async def get_levels():
    """Get list of all levels"""

    levels = []
    for level in LEVELS:
        levels.append({
            "level": level.level,
            "min_xp": level.min_xp,
            "max_xp": level.max_xp,
            "title": level.title
        })

    return APIResponse(
        success=True,
        data={"levels": levels},
        message="Levels retrieved successfully"
    )


# ===== MISSIONS ENDPOINTS =====

@router.get("/missions/daily/{user_id}", response_model=APIResponse)
async def get_daily_missions(user_id: str):
    """Get daily missions for a user"""

    try:
        # Expire old missions first
        mission_service.expire_old_missions(user_id)

        # Get today's missions
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

        return APIResponse(
            success=True,
            data={"missions": [m.dict() for m in missions_response]},
            message=f"Retrieved {len(missions)} missions for today"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/missions/{mission_id}/complete", response_model=APIResponse)
async def complete_mission(mission_id: str, user_id: str):
    """Complete a mission and award rewards"""

    try:
        result = mission_service.complete_mission(mission_id, user_id)

        # Get updated user XP and coins
        db = get_firestore_client()
        user_doc = db.collection('users').document(user_id).get()
        user_data = user_doc.to_dict()
        gamification = user_data.get('gamification', {})

        response = CompleteMissionResponse(
            success=True,
            mission_id=mission_id,
            xp_earned=result['xp_earned'],
            coins_earned=result['coins_earned'],
            total_xp=gamification.get('xp', 0),
            total_coins=result['total_coins'],
            level_up=result['level_up'],
            new_level=result['new_level'],
            message=f"Mission completed! Earned {result['xp_earned']} XP and {result['coins_earned']} coins!"
        )

        return APIResponse(
            success=True,
            data=response.dict(),
            message=response.message
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/missions/stats/{user_id}", response_model=APIResponse)
async def get_mission_stats(user_id: str):
    """Get mission statistics for a user"""

    try:
        stats = mission_service.get_mission_stats(user_id)

        return APIResponse(
            success=True,
            data=stats,
            message="Mission stats retrieved successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/missions/progress", response_model=APIResponse)
async def update_mission_progress(request: UpdateMissionProgressRequest):
    """
    Update mission progress by type.

    This endpoint increments the progress of a mission based on its type.
    If the mission reaches its target, it's automatically completed and rewards are given.

    Mission types:
    - daily_login: Fazer login diário
    - add_transaction: Registrar transações (target: 3)
    - complete_quiz: Completar um quiz
    - view_report: Ver relatório financeiro
    - chat_fim: Conversar com o FIM
    """
    try:
        # Map string type to MissionType enum
        type_mapping = {
            'daily_login': MissionType.DAILY_LOGIN,
            'add_transaction': MissionType.ADD_TRANSACTION,
            'complete_quiz': MissionType.COMPLETE_QUIZ,
            'view_report': MissionType.VIEW_REPORT,
            'chat_fim': MissionType.CHAT_FIM,
        }

        mission_type = type_mapping.get(request.mission_type.lower())
        if not mission_type:
            raise ValueError(f"Invalid mission type: {request.mission_type}")

        # Ensure daily missions exist for today
        mission_service.expire_old_missions(request.user_id)
        missions = mission_service.get_daily_missions(request.user_id)

        # Update progress
        updated_mission = mission_service.update_mission_progress(
            request.user_id,
            mission_type,
            increment=1
        )

        if not updated_mission:
            # Mission might already be completed or not found
            return APIResponse(
                success=True,
                data={
                    'mission_id': None,
                    'mission_type': request.mission_type,
                    'completed': False,
                    'message': 'Mission already completed or not found for today'
                },
                message='Mission already completed or not found for today'
            )

        # Check if mission was just completed (progress >= target)
        was_completed = updated_mission.status == MissionStatus.COMPLETED
        xp_earned = 0
        coins_earned = 0
        total_xp = None
        total_coins = None
        level_up = False
        new_level = None

        if was_completed:
            # Complete the mission to award rewards
            try:
                result = mission_service.complete_mission(updated_mission.id, request.user_id)
                xp_earned = result['xp_earned']
                coins_earned = result['coins_earned']
                total_coins = result['total_coins']
                level_up = result['level_up']
                new_level = result['new_level']

                # Get updated user stats
                db = get_firestore_client()
                user_doc = db.collection('users').document(request.user_id).get()
                user_data = user_doc.to_dict()
                gamification = user_data.get('gamification', {})
                total_xp = gamification.get('xp', 0)
            except ValueError:
                # Mission already completed, just return current state
                pass

        response = MissionProgressResponse(
            success=True,
            mission_id=updated_mission.id,
            mission_type=request.mission_type,
            title=updated_mission.title,
            progress=updated_mission.progress,
            target=updated_mission.target,
            completed=was_completed,
            xp_earned=xp_earned,
            coins_earned=coins_earned,
            total_xp=total_xp,
            total_coins=total_coins,
            level_up=level_up,
            new_level=new_level,
            message=f"Missão completada! +{xp_earned} XP, +{coins_earned} moedas!" if was_completed else f"Progresso atualizado: {updated_mission.progress}/{updated_mission.target}"
        )

        return APIResponse(
            success=True,
            data=response.dict(),
            message=response.message
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
