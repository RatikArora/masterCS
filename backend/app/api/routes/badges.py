"""Badge and achievement system — computed dynamically from user stats."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.subject import Topic
from app.models.concept import Concept
from app.models.progress import UserConceptProgress, UserQuestionAttempt
from pydantic import BaseModel

router = APIRouter(prefix="/badges", tags=["Badges"])


class Badge(BaseModel):
    id: str
    name: str
    description: str
    icon: str  # SVG icon name
    category: str  # xp, streak, mastery, accuracy, volume
    earned: bool
    progress: float  # 0.0 to 1.0
    current_value: int
    target_value: int


class LevelInfo(BaseModel):
    level: int
    title: str
    current_xp: int
    xp_for_next: int
    progress: float  # 0-1 within current level


class BadgesResponse(BaseModel):
    level: LevelInfo
    badges: list[Badge]
    total_earned: int
    total_available: int


# XP thresholds for levels
LEVELS = [
    (0, "Beginner"),
    (100, "Novice"),
    (300, "Learner"),
    (600, "Student"),
    (1000, "Scholar"),
    (1800, "Expert"),
    (3000, "Master"),
    (5000, "Grandmaster"),
    (8000, "Legend"),
    (12000, "Mythic"),
]


def _get_level(xp: int) -> LevelInfo:
    level = 1
    title = "Beginner"
    current_threshold = 0
    next_threshold = 100
    for i, (threshold, name) in enumerate(LEVELS):
        if xp >= threshold:
            level = i + 1
            title = name
            current_threshold = threshold
            next_threshold = LEVELS[i + 1][0] if i + 1 < len(LEVELS) else threshold + 5000
    progress = (xp - current_threshold) / max(next_threshold - current_threshold, 1)
    return LevelInfo(
        level=level, title=title, current_xp=xp,
        xp_for_next=next_threshold, progress=min(progress, 1.0),
    )


# Badge definitions: (id, name, desc, icon, category, target)
BADGE_DEFS = [
    # XP badges
    ("xp-100", "First Steps", "Earn 100 XP", "zap", "xp", 100),
    ("xp-500", "Getting Serious", "Earn 500 XP", "zap", "xp", 500),
    ("xp-1000", "XP Machine", "Earn 1,000 XP", "zap", "xp", 1000),
    ("xp-5000", "Knowledge Powerhouse", "Earn 5,000 XP", "zap", "xp", 5000),
    # Streak badges
    ("streak-3", "Hat Trick", "3-day streak", "flame", "streak", 3),
    ("streak-7", "Week Warrior", "7-day streak", "flame", "streak", 7),
    ("streak-14", "Fortnight Force", "14-day streak", "flame", "streak", 14),
    ("streak-30", "Monthly Master", "30-day streak", "flame", "streak", 30),
    ("streak-100", "Centurion", "100-day streak", "flame", "streak", 100),
    # Volume badges
    ("ans-10", "First Ten", "Answer 10 questions", "target", "volume", 10),
    ("ans-50", "Half Century", "Answer 50 questions", "target", "volume", 50),
    ("ans-100", "Century", "Answer 100 questions", "target", "volume", 100),
    ("ans-500", "Marathon Runner", "Answer 500 questions", "target", "volume", 500),
    # Mastery badges
    ("master-1", "First Mastery", "Master 1 concept", "award", "mastery", 1),
    ("master-5", "Quick Study", "Master 5 concepts", "award", "mastery", 5),
    ("master-10", "Knowledge Builder", "Master 10 concepts", "award", "mastery", 10),
    ("master-25", "Subject Expert", "Master 25 concepts", "award", "mastery", 25),
    # Accuracy badges
    ("acc-80", "Sharpshooter", "80%+ accuracy (50+ answers)", "crosshair", "accuracy", 80),
    ("acc-90", "Precision Expert", "90%+ accuracy (50+ answers)", "crosshair", "accuracy", 90),
    ("acc-95", "Near Perfect", "95%+ accuracy (100+ answers)", "crosshair", "accuracy", 95),
]


@router.get("", response_model=BadgesResponse)
def get_badges(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    level = _get_level(user.total_xp or 0)

    # Get user stats
    total_answers = (
        db.query(func.count(UserQuestionAttempt.id))
        .filter(UserQuestionAttempt.user_id == user.id)
        .scalar()
    ) or 0

    total_correct = (
        db.query(func.count(UserQuestionAttempt.id))
        .filter(UserQuestionAttempt.user_id == user.id, UserQuestionAttempt.is_correct == True)
        .scalar()
    ) or 0

    accuracy = (total_correct / total_answers * 100) if total_answers > 0 else 0

    mastered_count = (
        db.query(func.count(UserConceptProgress.id))
        .filter(
            UserConceptProgress.user_id == user.id,
            UserConceptProgress.mastery_level == "mastered",
        )
        .scalar()
    ) or 0

    badges: list[Badge] = []
    for bid, name, desc, icon, cat, target in BADGE_DEFS:
        if cat == "xp":
            current = user.total_xp or 0
        elif cat == "streak":
            current = user.longest_streak or 0
        elif cat == "volume":
            current = total_answers
        elif cat == "mastery":
            current = mastered_count
        elif cat == "accuracy":
            current = int(accuracy) if total_answers >= (100 if target >= 95 else 50) else 0
        else:
            current = 0

        earned = current >= target
        progress = min(current / max(target, 1), 1.0)

        badges.append(Badge(
            id=bid, name=name, description=desc, icon=icon,
            category=cat, earned=earned, progress=progress,
            current_value=current, target_value=target,
        ))

    total_earned = sum(1 for b in badges if b.earned)
    return BadgesResponse(
        level=level, badges=badges,
        total_earned=total_earned, total_available=len(badges),
    )
