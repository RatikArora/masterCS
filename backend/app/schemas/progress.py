from pydantic import BaseModel
from datetime import datetime


class OverallProgress(BaseModel):
    total_concepts: int
    concepts_started: int
    concepts_mastered: int
    total_questions_answered: int
    overall_accuracy: float
    current_streak: int
    longest_streak: int
    total_xp: int
    mastery_distribution: dict[str, int]  # {"novice": 10, "learning": 5, ...}


class TopicProgress(BaseModel):
    topic_id: str
    topic_name: str
    total_concepts: int
    mastered_concepts: int
    avg_confidence: float
    mastery_percent: float


class ConceptProgressDetail(BaseModel):
    concept_id: str
    concept_name: str
    topic_name: str
    mastery_level: str
    confidence_score: float
    exposure_count: int
    correct_count: int
    incorrect_count: int
    accuracy: float
    last_seen_at: datetime | None
    next_review_at: datetime | None
    error_streak: int


class WeakAreaResponse(BaseModel):
    concept_id: str
    concept_name: str
    topic_name: str
    confidence_score: float
    error_streak: int
    accuracy: float
    recommended_action: str


class DailyStatsResponse(BaseModel):
    date: str
    questions_answered: int
    correct_count: int
    accuracy: float
    xp_earned: int
    time_spent_minutes: float


class StreakResponse(BaseModel):
    current_streak: int
    longest_streak: int
    today_completed: bool
    daily_goal: int
    questions_today: int
