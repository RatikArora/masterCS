from sqlalchemy import (
    Column, String, Integer, Float, DateTime, Boolean, ForeignKey, Date, func, Index,
    UniqueConstraint,
)
from app.db.base import Base


class UserConceptProgress(Base):
    __tablename__ = "user_concept_progress"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    concept_id = Column(String(36), ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False)

    confidence_score = Column(Float, default=0.0)
    exposure_count = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    incorrect_count = Column(Integer, default=0)
    avg_response_time_ms = Column(Integer, default=0)

    # Spaced repetition fields
    ease_factor = Column(Float, default=2.5)
    interval_days = Column(Integer, default=0)
    repetition_number = Column(Integer, default=0)
    last_seen_at = Column(DateTime, nullable=True)
    next_review_at = Column(DateTime, nullable=True)

    error_streak = Column(Integer, default=0)
    correct_streak = Column(Integer, default=0)
    mastery_level = Column(String(20), default="novice")

    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "concept_id", name="uq_user_concept"),
        Index("ix_ucp_user_concept", "user_id", "concept_id"),
        Index("ix_ucp_user_mastery", "user_id", "mastery_level"),
        Index("ix_ucp_user_confidence", "user_id", "confidence_score"),
        Index("ix_ucp_next_review", "user_id", "next_review_at"),
    )


class UserQuestionAttempt(Base):
    __tablename__ = "user_question_attempts"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    concept_id = Column(String(36), ForeignKey("concepts.id", ondelete="SET NULL"), nullable=True)
    selected_answer = Column(String(500), nullable=True)
    is_correct = Column(Boolean, nullable=False)
    response_time_ms = Column(Integer, default=0)
    difficulty_at_time = Column(Integer, default=1)
    attempted_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_uqa_user_time", "user_id", "attempted_at"),
        Index("ix_uqa_user_question", "user_id", "question_id"),
        Index("ix_uqa_user_correct", "user_id", "is_correct"),
    )


class UserDailyStats(Base):
    __tablename__ = "user_daily_stats"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    questions_answered = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    time_spent_seconds = Column(Integer, default=0)
    xp_earned = Column(Integer, default=0)
    streak_day = Column(Integer, default=0)

    __table_args__ = (
        UniqueConstraint("user_id", "date", name="uq_user_date"),
        Index("ix_uds_user_date", "user_id", "date"),
    )
