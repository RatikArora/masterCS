from pydantic import BaseModel
from datetime import datetime


class SubjectResponse(BaseModel):
    id: str
    name: str
    description: str | None
    icon: str | None
    color: str | None
    order_index: int
    topic_count: int = 0
    progress_percent: float = 0.0

    class Config:
        from_attributes = True


class TopicResponse(BaseModel):
    id: str
    subject_id: str
    name: str
    description: str | None
    icon: str | None
    order_index: int
    concept_count: int = 0
    mastery_percent: float = 0.0
    is_unlocked: bool = True

    class Config:
        from_attributes = True


class ConceptResponse(BaseModel):
    id: str
    topic_id: str
    name: str
    explanation: str | None
    key_points: list[str] | None
    order_index: int
    mastery_level: str = "novice"
    confidence_score: float = 0.0

    class Config:
        from_attributes = True


class ConceptDetailResponse(ConceptResponse):
    topic_name: str = ""
    subject_name: str = ""
    question_count: int = 0
    attempts_count: int = 0
    accuracy: float = 0.0
