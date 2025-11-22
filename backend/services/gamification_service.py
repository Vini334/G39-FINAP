"""
Gamification Service
Business logic for gamification system (XP, levels, lives, coins, challenges).
"""

from datetime import datetime, timedelta
from typing import Optional, List, Tuple, Dict
from core.database import get_firestore_client
from models.gamification import (
    XPAction, XP_REWARDS, LEVELS, LivesConfig,
    XPTransaction, Challenge, ChallengeStatus, ChallengeType,
    COINS_REWARDS, Level
)
from models.user import UserGamification
import uuid


class GamificationService:
    """Service for managing gamification features"""

    def __init__(self):
        self.db = get_firestore_client()
        self.lives_config = LivesConfig()

    def add_xp(self, user_id: str, action: XPAction, metadata: Dict = None) -> Tuple[int, bool, Optional[int]]:
        """
        Add XP to user for an action.

        Returns:
            Tuple of (xp_added, level_up, new_level)
        """
        if action not in XP_REWARDS:
            raise ValueError(f"Invalid XP action: {action}")

        reward = XP_REWARDS[action]
        xp_amount = reward.amount

        # Get user document
        user_ref = self.db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            raise ValueError(f"User {user_id} not found")

        user_data = user_doc.to_dict()
        gamification = user_data.get('gamification', {})

        # Calculate new XP and level
        current_xp = gamification.get('xp', 0)
        current_level = gamification.get('level', 1)
        new_xp = current_xp + xp_amount

        # Check for level up
        level_up = False
        new_level = current_level

        for level in LEVELS:
            if new_xp >= level.min_xp:
                if level.max_xp is None or new_xp <= level.max_xp:
                    new_level = level.level
                    break

        if new_level > current_level:
            level_up = True

        # Update user gamification
        user_ref.update({
            'gamification.xp': new_xp,
            'gamification.level': new_level,
            'updated_at': datetime.now()
        })

        # Record XP transaction
        xp_transaction = XPTransaction(
            id=str(uuid.uuid4()),
            user_id=user_id,
            action=action,
            xp_amount=xp_amount,
            description=reward.description,
            metadata=metadata or {},
            created_at=datetime.now()
        )

        self.db.collection('xp_transactions').document(xp_transaction.id).set(
            xp_transaction.dict()
        )

        return xp_amount, level_up, new_level if level_up else None

    def get_level_info(self, xp: int) -> Level:
        """Get level information for given XP"""
        for level in LEVELS:
            if level.max_xp is None:
                if xp >= level.min_xp:
                    return level
            elif level.min_xp <= xp <= level.max_xp:
                return level
        return LEVELS[0]

    def calculate_xp_to_next_level(self, current_xp: int, current_level: int) -> Optional[int]:
        """Calculate XP needed for next level"""
        if current_level >= len(LEVELS):
            return None

        current_level_data = LEVELS[current_level - 1]
        if current_level_data.max_xp is None:
            return None

        return current_level_data.max_xp - current_xp + 1

    def calculate_progress_percentage(self, current_xp: int, level: int) -> int:
        """Calculate progress percentage within current level"""
        if level > len(LEVELS):
            return 100

        level_data = LEVELS[level - 1]

        if level_data.max_xp is None:
            return 100

        xp_in_level = current_xp - level_data.min_xp
        level_range = level_data.max_xp - level_data.min_xp + 1

        return min(100, int((xp_in_level / level_range) * 100))

    def spend_lives(self, user_id: str, amount: int = 1) -> Tuple[int, Optional[datetime]]:
        """
        Spend user lives.

        Returns:
            Tuple of (remaining_lives, next_recharge_time)
        """
        user_ref = self.db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            raise ValueError(f"User {user_id} not found")

        user_data = user_doc.to_dict()
        gamification = user_data.get('gamification', {})

        current_lives = gamification.get('lives', 5)

        if current_lives < amount:
            raise ValueError(f"Not enough lives. Current: {current_lives}, Required: {amount}")

        new_lives = current_lives - amount

        # Calculate next recharge time
        next_recharge = None
        if new_lives < self.lives_config.max_lives:
            next_recharge = datetime.now() + timedelta(hours=self.lives_config.recharge_time_hours)

        # Update user
        update_data = {
            'gamification.lives': new_lives,
            'updated_at': datetime.now()
        }

        if 'lives_last_recharge' not in gamification:
            update_data['gamification.lives_last_recharge'] = datetime.now()

        user_ref.update(update_data)

        return new_lives, next_recharge

    def recharge_lives(self, user_id: str) -> int:
        """
        Recharge lives based on time elapsed.

        Returns:
            Current lives after recharge
        """
        user_ref = self.db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            raise ValueError(f"User {user_id} not found")

        user_data = user_doc.to_dict()
        gamification = user_data.get('gamification', {})

        current_lives = gamification.get('lives', 5)
        last_recharge = gamification.get('lives_last_recharge', datetime.now())

        # If already at max, no recharge needed
        if current_lives >= self.lives_config.max_lives:
            return current_lives

        # Calculate lives to add based on time elapsed
        if isinstance(last_recharge, str):
            last_recharge = datetime.fromisoformat(last_recharge.replace('Z', '+00:00'))

        time_elapsed = datetime.now() - last_recharge
        hours_elapsed = time_elapsed.total_seconds() / 3600
        lives_to_add = int(hours_elapsed / self.lives_config.recharge_time_hours)

        if lives_to_add > 0:
            new_lives = min(current_lives + lives_to_add, self.lives_config.max_lives)

            user_ref.update({
                'gamification.lives': new_lives,
                'gamification.lives_last_recharge': datetime.now(),
                'updated_at': datetime.now()
            })

            return new_lives

        return current_lives

    def award_coins(self, user_id: str, amount: int, reason: str) -> int:
        """
        Award coins to user.

        Returns:
            Total coins after award
        """
        user_ref = self.db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            raise ValueError(f"User {user_id} not found")

        user_data = user_doc.to_dict()
        gamification = user_data.get('gamification', {})
        current_coins = gamification.get('coins', 0)

        new_coins = current_coins + amount

        user_ref.update({
            'gamification.coins': new_coins,
            'updated_at': datetime.now()
        })

        return new_coins

    def spend_coins(self, user_id: str, amount: int, reason: str) -> int:
        """
        Spend user coins.

        Returns:
            Remaining coins
        """
        user_ref = self.db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            raise ValueError(f"User {user_id} not found")

        user_data = user_doc.to_dict()
        gamification = user_data.get('gamification', {})
        current_coins = gamification.get('coins', 0)

        if current_coins < amount:
            raise ValueError(f"Not enough coins. Current: {current_coins}, Required: {amount}")

        new_coins = current_coins - amount

        user_ref.update({
            'gamification.coins': new_coins,
            'updated_at': datetime.now()
        })

        return new_coins

    def create_challenge(
        self,
        user_id: str,
        challenge_type: ChallengeType,
        title: str,
        description: str,
        target: float,
        reward_xp: int = 100,
        reward_coins: int = 50,
        duration_days: int = 7
    ) -> Challenge:
        """Create a new challenge for user"""

        challenge = Challenge(
            id=str(uuid.uuid4()),
            user_id=user_id,
            type=challenge_type,
            title=title,
            description=description,
            target=target,
            current=0.0,
            reward_xp=reward_xp,
            reward_coins=reward_coins,
            status=ChallengeStatus.ACTIVE,
            starts_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=duration_days),
            created_at=datetime.now()
        )

        self.db.collection('challenges').document(challenge.id).set(challenge.dict())

        return challenge

    def update_challenge_progress(self, challenge_id: str, progress: float) -> Challenge:
        """Update challenge progress"""

        challenge_ref = self.db.collection('challenges').document(challenge_id)
        challenge_doc = challenge_ref.get()

        if not challenge_doc.exists:
            raise ValueError(f"Challenge {challenge_id} not found")

        challenge_data = challenge_doc.to_dict()
        challenge = Challenge(**challenge_data)

        # Check if challenge is still active
        if challenge.status != ChallengeStatus.ACTIVE:
            raise ValueError(f"Challenge is not active. Current status: {challenge.status}")

        # Check if expired
        if datetime.now() > challenge.expires_at:
            challenge_ref.update({
                'status': ChallengeStatus.EXPIRED,
                'updated_at': datetime.now()
            })
            challenge.status = ChallengeStatus.EXPIRED
            return challenge

        # Update progress
        new_progress = min(progress, challenge.target)
        challenge_ref.update({
            'current': new_progress,
            'updated_at': datetime.now()
        })
        challenge.current = new_progress

        # Check if completed
        if new_progress >= challenge.target:
            challenge_ref.update({
                'status': ChallengeStatus.COMPLETED,
                'completed_at': datetime.now(),
                'updated_at': datetime.now()
            })
            challenge.status = ChallengeStatus.COMPLETED
            challenge.completed_at = datetime.now()

            # Award XP and coins
            self.add_xp(challenge.user_id, XPAction.COMPLETE_CHALLENGE, {'challenge_id': challenge_id})
            self.award_coins(challenge.user_id, challenge.reward_coins, f"Completed challenge: {challenge.title}")

        return challenge

    def get_user_challenges(self, user_id: str) -> Dict[str, List[Challenge]]:
        """Get all user challenges grouped by status"""

        challenges_ref = self.db.collection('challenges').where('user_id', '==', user_id)
        challenges_docs = challenges_ref.stream()

        active = []
        completed = []
        expired = []

        for doc in challenges_docs:
            challenge_data = doc.to_dict()
            challenge = Challenge(**challenge_data)

            # Auto-expire if past expiration date
            if challenge.status == ChallengeStatus.ACTIVE and datetime.now() > challenge.expires_at:
                self.db.collection('challenges').document(challenge.id).update({
                    'status': ChallengeStatus.EXPIRED,
                    'updated_at': datetime.now()
                })
                challenge.status = ChallengeStatus.EXPIRED

            if challenge.status == ChallengeStatus.ACTIVE:
                active.append(challenge)
            elif challenge.status == ChallengeStatus.COMPLETED:
                completed.append(challenge)
            elif challenge.status == ChallengeStatus.EXPIRED:
                expired.append(challenge)

        return {
            'active': active,
            'completed': completed,
            'expired': expired
        }

    def update_streak(self, user_id: str) -> int:
        """Update user's login streak"""

        user_ref = self.db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            raise ValueError(f"User {user_id} not found")

        user_data = user_doc.to_dict()
        gamification = user_data.get('gamification', {})

        last_login = gamification.get('last_login', datetime.now())
        if isinstance(last_login, str):
            last_login = datetime.fromisoformat(last_login.replace('Z', '+00:00'))

        current_streak = gamification.get('current_streak', 0)
        longest_streak = gamification.get('longest_streak', 0)

        # Calculate time difference
        now = datetime.now()
        time_diff = now - last_login

        # If more than 1 day, reset streak
        if time_diff.days > 1:
            current_streak = 1
        # If same day, don't increment
        elif time_diff.days < 1:
            current_streak = current_streak  # Keep same
        # If exactly 1 day, increment
        else:
            current_streak += 1

        # Update longest streak
        if current_streak > longest_streak:
            longest_streak = current_streak

        # Award XP for 7-day streak
        if current_streak == 7:
            self.add_xp(user_id, XPAction.MAINTAIN_STREAK_7, {'streak': 7})

        user_ref.update({
            'gamification.current_streak': current_streak,
            'gamification.longest_streak': longest_streak,
            'gamification.last_login': now,
            'updated_at': now
        })

        return current_streak
