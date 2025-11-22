"""
Mission Service
Business logic for daily missions system.
"""

from datetime import datetime, date
from typing import List, Optional, Dict
from core.database import get_firestore_client
from models.gamification import (
    Mission, MissionType, MissionStatus, XPAction
)
from services.gamification_service import GamificationService
import uuid


class MissionService:
    """Service for managing daily missions"""

    def __init__(self):
        self.db = get_firestore_client()
        self.gamification_service = GamificationService()

    def _get_today_date(self) -> str:
        """Get today's date in YYYY-MM-DD format"""
        return date.today().strftime("%Y-%m-%d")

    def generate_daily_missions(self, user_id: str) -> List[Mission]:
        """
        Generate daily missions for a user.
        This creates a standard set of missions that reset daily.
        """
        today = self._get_today_date()

        # Standard daily missions
        mission_templates = [
            {
                "type": MissionType.DAILY_LOGIN,
                "title": "Fazer login diário",
                "description": "Entre no app e ganhe XP",
                "xp_reward": 10,
                "coins_reward": 5,
                "target": 1,
            },
            {
                "type": MissionType.ADD_TRANSACTION,
                "title": "Registrar 3 transações",
                "description": "Adicione 3 transações hoje",
                "xp_reward": 15,
                "coins_reward": 10,
                "target": 3,
            },
            {
                "type": MissionType.COMPLETE_QUIZ,
                "title": "Completar um quiz",
                "description": "Responda um quiz de aprendizado",
                "xp_reward": 30,
                "coins_reward": 20,
                "target": 1,
            },
            {
                "type": MissionType.VIEW_REPORT,
                "title": "Ver relatório financeiro",
                "description": "Revise seus gastos do mês",
                "xp_reward": 25,
                "coins_reward": 15,
                "target": 1,
            },
            {
                "type": MissionType.CHAT_FIM,
                "title": "Conversar com o FIM",
                "description": "Envie uma mensagem ao FIM",
                "xp_reward": 20,
                "coins_reward": 10,
                "target": 1,
            },
        ]

        missions = []
        for template in mission_templates:
            mission = Mission(
                id=str(uuid.uuid4()),
                user_id=user_id,
                type=template["type"],
                title=template["title"],
                description=template["description"],
                xp_reward=template["xp_reward"],
                coins_reward=template["coins_reward"],
                status=MissionStatus.PENDING,
                progress=0,
                target=template["target"],
                date=today,
                created_at=datetime.now()
            )
            missions.append(mission)

            # Save to Firestore
            self.db.collection('missions').document(mission.id).set(mission.dict())

        return missions

    def get_daily_missions(self, user_id: str) -> List[Mission]:
        """
        Get daily missions for a user.
        Creates new missions if none exist for today.
        """
        today = self._get_today_date()

        # Check if missions exist for today
        missions_ref = self.db.collection('missions') \
            .where('user_id', '==', user_id) \
            .where('date', '==', today)

        missions_docs = list(missions_ref.stream())

        # If no missions for today, generate them
        if not missions_docs:
            return self.generate_daily_missions(user_id)

        # Return existing missions
        missions = []
        for doc in missions_docs:
            mission_data = doc.to_dict()
            missions.append(Mission(**mission_data))

        # Sort by status (pending first)
        missions.sort(key=lambda m: (m.status != MissionStatus.PENDING, m.created_at))

        return missions

    def update_mission_progress(
        self,
        user_id: str,
        mission_type: MissionType,
        increment: int = 1
    ) -> Optional[Mission]:
        """
        Update mission progress for a specific type.
        Automatically completes the mission if target is reached.
        """
        today = self._get_today_date()

        # Find mission
        missions_ref = self.db.collection('missions') \
            .where('user_id', '==', user_id) \
            .where('type', '==', mission_type.value) \
            .where('date', '==', today) \
            .where('status', '==', MissionStatus.PENDING.value)

        missions_docs = list(missions_ref.stream())

        if not missions_docs:
            return None

        # Get first matching mission
        mission_doc = missions_docs[0]
        mission_data = mission_doc.to_dict()
        mission = Mission(**mission_data)

        # Update progress
        new_progress = min(mission.progress + increment, mission.target)

        update_data = {
            'progress': new_progress,
            'updated_at': datetime.now()
        }

        # Check if completed
        if new_progress >= mission.target:
            update_data['status'] = MissionStatus.COMPLETED.value
            update_data['completed_at'] = datetime.now()

            mission.status = MissionStatus.COMPLETED
            mission.completed_at = datetime.now()

        self.db.collection('missions').document(mission.id).update(update_data)
        mission.progress = new_progress

        return mission

    def complete_mission(self, mission_id: str, user_id: str) -> Dict:
        """
        Manually complete a mission.
        Awards XP and coins to the user.
        """
        mission_ref = self.db.collection('missions').document(mission_id)
        mission_doc = mission_ref.get()

        if not mission_doc.exists:
            raise ValueError(f"Mission {mission_id} not found")

        mission_data = mission_doc.to_dict()
        mission = Mission(**mission_data)

        # Verify ownership
        if mission.user_id != user_id:
            raise ValueError("Mission does not belong to user")

        # Check if already completed
        if mission.status == MissionStatus.COMPLETED:
            raise ValueError("Mission already completed")

        # Check if expired
        today = self._get_today_date()
        if mission.date != today:
            mission_ref.update({
                'status': MissionStatus.EXPIRED.value,
                'updated_at': datetime.now()
            })
            raise ValueError("Mission has expired")

        # Mark as completed
        mission_ref.update({
            'status': MissionStatus.COMPLETED.value,
            'progress': mission.target,
            'completed_at': datetime.now(),
            'updated_at': datetime.now()
        })

        # Award XP based on mission type
        xp_action_map = {
            MissionType.DAILY_LOGIN: XPAction.DAILY_LOGIN,
            MissionType.ADD_TRANSACTION: XPAction.ADD_TRANSACTION,
            MissionType.COMPLETE_QUIZ: XPAction.COMPLETE_QUIZ,
            MissionType.VIEW_REPORT: XPAction.REVIEW_MONTHLY_REPORT,
        }

        xp_action = xp_action_map.get(mission.type)
        if xp_action:
            xp_earned, level_up, new_level = self.gamification_service.add_xp(
                user_id,
                xp_action,
                {'mission_id': mission_id}
            )
        else:
            xp_earned = mission.xp_reward
            level_up = False
            new_level = None

        # Award coins
        coins_earned = self.gamification_service.award_coins(
            user_id,
            mission.coins_reward,
            f"Completed mission: {mission.title}"
        )

        return {
            'mission_id': mission_id,
            'xp_earned': xp_earned,
            'coins_earned': mission.coins_reward,
            'total_coins': coins_earned,
            'level_up': level_up,
            'new_level': new_level,
            'mission_title': mission.title
        }

    def expire_old_missions(self, user_id: str) -> int:
        """
        Expire missions from previous days.
        Returns count of expired missions.
        """
        today = self._get_today_date()

        # Find pending missions from previous days
        missions_ref = self.db.collection('missions') \
            .where('user_id', '==', user_id) \
            .where('status', '==', MissionStatus.PENDING.value)

        missions_docs = missions_ref.stream()

        expired_count = 0
        for doc in missions_docs:
            mission_data = doc.to_dict()
            mission = Mission(**mission_data)

            if mission.date != today:
                self.db.collection('missions').document(mission.id).update({
                    'status': MissionStatus.EXPIRED.value,
                    'updated_at': datetime.now()
                })
                expired_count += 1

        return expired_count

    def get_mission_stats(self, user_id: str) -> Dict:
        """
        Get mission statistics for a user.
        """
        # Get all completed missions
        missions_ref = self.db.collection('missions') \
            .where('user_id', '==', user_id) \
            .where('status', '==', MissionStatus.COMPLETED.value)

        missions_docs = list(missions_ref.stream())

        total_completed = len(missions_docs)
        total_xp_earned = sum(Mission(**doc.to_dict()).xp_reward for doc in missions_docs)
        total_coins_earned = sum(Mission(**doc.to_dict()).coins_reward for doc in missions_docs)

        # Get today's missions
        today = self._get_today_date()
        today_missions = self.get_daily_missions(user_id)
        today_completed = sum(1 for m in today_missions if m.status == MissionStatus.COMPLETED)

        return {
            'total_completed': total_completed,
            'total_xp_earned': total_xp_earned,
            'total_coins_earned': total_coins_earned,
            'today_total': len(today_missions),
            'today_completed': today_completed,
            'today_completion_rate': round(today_completed / len(today_missions) * 100) if today_missions else 0
        }
