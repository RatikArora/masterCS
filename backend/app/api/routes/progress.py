"""Progress and statistics routes — optimized queries with pagination."""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.core.pagination import PaginationParams, PaginatedResponse, paginate_query
from app.models.user import User
from app.models.subject import Subject, Topic
from app.models.concept import Concept
from app.models.progress import UserConceptProgress, UserQuestionAttempt, UserDailyStats
from app.schemas.progress import (
    OverallProgress, TopicProgress, ConceptProgressDetail,
    WeakAreaResponse, DailyStatsResponse, StreakResponse,
)

router = APIRouter(prefix="/progress", tags=["Progress"])

DAILY_GOAL = 10


def _get_subject_concept_ids_subquery(subject_id: str):
    """Reusable subquery for concept IDs within a subject."""
    from sqlalchemy import select
    return (
        select(Concept.id)
        .join(Topic, Concept.topic_id == Topic.id)
        .where(Topic.subject_id == subject_id)
        .scalar_subquery()
    )


@router.get("/overview/{subject_id}", response_model=OverallProgress)
def get_overview(
    subject_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Overall progress — aggregated in two queries max."""
    # Total concepts in subject
    total_concepts = (
        db.query(func.count(Concept.id))
        .join(Topic, Concept.topic_id == Topic.id)
        .filter(Topic.subject_id == subject_id)
        .scalar()
    ) or 0

    # Aggregated progress stats in single query
    progress_stats = (
        db.query(
            func.count(UserConceptProgress.id).label("started"),
            func.sum(case((UserConceptProgress.mastery_level == "mastered", 1), else_=0)).label("mastered"),
            func.sum(case((UserConceptProgress.mastery_level == "novice", 1), else_=0)).label("novice_count"),
            func.sum(case((UserConceptProgress.mastery_level == "learning", 1), else_=0)).label("learning_count"),
            func.sum(case((UserConceptProgress.mastery_level == "familiar", 1), else_=0)).label("familiar_count"),
            func.sum(case((UserConceptProgress.mastery_level == "proficient", 1), else_=0)).label("proficient_count"),
            func.coalesce(func.sum(case(
                (UserConceptProgress.mastery_level == "mastered", 1.0),
                (UserConceptProgress.mastery_level == "proficient", 0.8),
                (UserConceptProgress.mastery_level == "familiar", 0.5),
                (UserConceptProgress.mastery_level == "learning", 0.2),
                else_=0.0,
            )), 0.0).label("weighted_score"),
        )
        .join(Concept, UserConceptProgress.concept_id == Concept.id)
        .join(Topic, Concept.topic_id == Topic.id)
        .filter(Topic.subject_id == subject_id, UserConceptProgress.user_id == user.id)
        .first()
    )

    started = int(progress_stats[0] or 0)
    mastered = int(progress_stats[1] or 0)
    weighted_score = float(progress_stats[6] or 0.0)

    # Attempt stats — scoped to this subject via concept_id join
    subject_concept_ids = (
        db.query(Concept.id)
        .join(Topic, Concept.topic_id == Topic.id)
        .filter(Topic.subject_id == subject_id)
        .subquery()
    )
    attempt_stats = (
        db.query(
            func.count(UserQuestionAttempt.id),
            func.sum(case((UserQuestionAttempt.is_correct == True, 1), else_=0)),
        )
        .filter(
            UserQuestionAttempt.user_id == user.id,
            UserQuestionAttempt.concept_id.in_(subject_concept_ids.select()),
        )
        .first()
    )

    total_answered = int(attempt_stats[0] or 0)
    total_correct = int(attempt_stats[1] or 0)
    accuracy = min((total_correct / total_answered * 100), 100.0) if total_answered > 0 else 0.0

    # Calculate subject-specific XP from attempts
    # Use stored xp_earned if available, otherwise estimate from difficulty
    subject_xp = (
        db.query(
            func.coalesce(
                func.sum(
                    case(
                        (UserQuestionAttempt.xp_earned > 0, UserQuestionAttempt.xp_earned),
                        (UserQuestionAttempt.is_correct == False, 2),
                        (UserQuestionAttempt.difficulty_at_time == 1, 10),
                        (UserQuestionAttempt.difficulty_at_time == 2, 20),
                        (UserQuestionAttempt.difficulty_at_time == 3, 35),
                        else_=10,
                    )
                ),
                0,
            )
        )
        .filter(
            UserQuestionAttempt.user_id == user.id,
            UserQuestionAttempt.concept_id.in_(subject_concept_ids.select()),
        )
        .scalar()
    ) or 0

    # Include both unstarted concepts and started-but-novice in novice count
    novice_from_progress = int(progress_stats[2] or 0)
    distribution = {
        "novice": (total_concepts - started) + novice_from_progress,
        "learning": int(progress_stats[3] or 0),
        "familiar": int(progress_stats[4] or 0),
        "proficient": int(progress_stats[5] or 0),
        "mastered": mastered,
    }

    return OverallProgress(
        total_concepts=total_concepts,
        concepts_started=started,
        concepts_mastered=mastered,
        total_questions_answered=total_answered,
        overall_accuracy=round(accuracy, 1),
        current_streak=user.current_streak,
        longest_streak=user.longest_streak,
        total_xp=int(subject_xp),
        mastery_distribution=distribution,
        weighted_progress=round((weighted_score / total_concepts) * 100, 1) if total_concepts > 0 else 0.0,
    )


@router.get("/topics/{subject_id}", response_model=list[TopicProgress])
def get_topic_progress(
    subject_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Per-topic progress — single aggregation query, no N+1."""
    # Weighted mastery: mastered=1.0, proficient=0.8, familiar=0.5, learning=0.2, novice=0
    rows = (
        db.query(
            Topic.id,
            Topic.name,
            func.count(Concept.id).label("total"),
            func.sum(case(
                (UserConceptProgress.mastery_level.in_(["proficient", "mastered"]), 1),
                else_=0,
            )).label("mastered_count"),
            func.coalesce(func.avg(UserConceptProgress.confidence_score), 0).label("avg_conf"),
            func.sum(case(
                (UserConceptProgress.mastery_level == "mastered", 1.0),
                (UserConceptProgress.mastery_level == "proficient", 0.8),
                (UserConceptProgress.mastery_level == "familiar", 0.5),
                (UserConceptProgress.mastery_level == "learning", 0.2),
                else_=0.0,
            )).label("weighted_sum"),
        )
        .join(Concept, Concept.topic_id == Topic.id)
        .outerjoin(
            UserConceptProgress,
            (UserConceptProgress.concept_id == Concept.id) & (UserConceptProgress.user_id == user.id),
        )
        .filter(Topic.subject_id == subject_id)
        .group_by(Topic.id, Topic.name)
        .order_by(Topic.order_index)
        .all()
    )

    return [
        TopicProgress(
            topic_id=tid, topic_name=tname, total_concepts=total,
            mastered_concepts=int(mc or 0),
            avg_confidence=round(float(ac), 3),
            mastery_percent=round((float(ws or 0) / total) * 100, 1) if total > 0 else 0.0,
        )
        for tid, tname, total, mc, ac, ws in rows
    ]


@router.get("/weak-areas/{subject_id}", response_model=PaginatedResponse[WeakAreaResponse])
def get_weak_areas(
    subject_id: str,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Weak areas — paginated, single joined query."""
    base_query = (
        db.query(UserConceptProgress, Concept.name, Topic.name)
        .join(Concept, UserConceptProgress.concept_id == Concept.id)
        .join(Topic, Concept.topic_id == Topic.id)
        .filter(
            Topic.subject_id == subject_id,
            UserConceptProgress.user_id == user.id,
            UserConceptProgress.confidence_score < 0.5,
            UserConceptProgress.exposure_count > 0,
        )
        .order_by(UserConceptProgress.confidence_score.asc())
    )

    total = base_query.count()
    rows = base_query.offset(pagination.offset).limit(pagination.page_size).all()

    items = []
    for progress, concept_name, topic_name in rows:
        total_attempts = progress.correct_count + progress.incorrect_count
        accuracy = min((progress.correct_count / total_attempts * 100), 100.0) if total_attempts > 0 else 0.0

        if progress.error_streak >= 3:
            action = "Needs immediate review — multiple consecutive errors"
        elif progress.confidence_score < 0.2:
            action = "Re-learn this concept from scratch"
        else:
            action = "Practice more questions on this topic"

        items.append(WeakAreaResponse(
            concept_id=progress.concept_id,
            concept_name=concept_name,
            topic_name=topic_name,
            confidence_score=round(progress.confidence_score, 3),
            error_streak=progress.error_streak,
            accuracy=round(accuracy, 1),
            recommended_action=action,
        ))

    return PaginatedResponse.create(items, total, pagination)


@router.get("/daily-stats", response_model=PaginatedResponse[DailyStatsResponse])
def get_daily_stats(
    days: int = 30,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Daily stats with pagination."""
    cutoff = datetime.utcnow().date() - timedelta(days=days)
    query = (
        db.query(UserDailyStats)
        .filter(UserDailyStats.user_id == user.id, UserDailyStats.date >= cutoff)
        .order_by(UserDailyStats.date.desc())
    )

    items, total = paginate_query(query, pagination)

    stats = [
        DailyStatsResponse(
            date=str(s.date),
            questions_answered=s.questions_answered,
            correct_count=s.correct_count,
            accuracy=round((s.correct_count / s.questions_answered * 100) if s.questions_answered > 0 else 0, 1),
            xp_earned=s.xp_earned,
            time_spent_minutes=round(s.time_spent_seconds / 60, 1),
        )
        for s in items
    ]

    return PaginatedResponse.create(stats, total, pagination)


@router.get("/streak", response_model=StreakResponse)
def get_streak(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    today = datetime.utcnow().date()
    today_stats = (
        db.query(UserDailyStats)
        .filter(UserDailyStats.user_id == user.id, UserDailyStats.date == today)
        .first()
    )

    return StreakResponse(
        current_streak=user.current_streak,
        longest_streak=user.longest_streak,
        today_completed=(today_stats.questions_answered >= DAILY_GOAL) if today_stats else False,
        daily_goal=DAILY_GOAL,
        questions_today=today_stats.questions_answered if today_stats else 0,
        xp_today=today_stats.xp_earned if today_stats else 0,
    )
