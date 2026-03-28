from pydantic import BaseModel


class QuestionResponse(BaseModel):
    id: str
    question_text: str
    question_type: str
    options: list[str] | None
    difficulty: int
    concept_id: str
    concept_name: str
    topic_name: str
    time_estimate_seconds: int
    attempt_number: int = 0  # how many times user has seen this question

    class Config:
        from_attributes = True


class AnswerSubmit(BaseModel):
    question_id: str
    selected_answer: str
    response_time_ms: int


class AnswerResult(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: str | None
    xp_earned: int
    confidence_change: float
    mastery_level: str
    streak_count: int
    next_review_message: str
    # Gamification extras
    level_up: bool = False
    new_badges: list[str] = []  # badge names just earned
    lesson_card: "LessonCard | None" = None
    cooldown_seconds: int | None = None  # seconds until this wrong Q respawns


class LessonCard(BaseModel):
    """Mini-lesson shown between questions."""
    title: str
    content: str  # markdown
    key_points: list[str]
    type: str  # "intro" | "review" | "mistake_fix"


class CooldownItem(BaseModel):
    question_id: str
    expires_in_seconds: int


class LearningSession(BaseModel):
    question: QuestionResponse
    session_stats: "SessionStats"
    concept_progress: "ConceptProgressBrief"
    cooldown_questions: list[CooldownItem] = []


class SessionStats(BaseModel):
    questions_answered_today: int
    correct_today: int
    current_streak: int
    xp_today: int


class ConceptProgressBrief(BaseModel):
    concept_id: str
    concept_name: str
    mastery_level: str
    confidence_score: float
    exposure_count: int


class WrongQuestionItem(BaseModel):
    question_id: str
    question_text: str
    correct_answer: str
    selected_answer: str
    explanation: str | None
    concept_id: str
    concept_name: str
    topic_name: str
    difficulty: int
    attempt_count: int
    last_attempted: str


class ReportSubmit(BaseModel):
    question_id: str
    reason: str  # wrong_answer, unclear, duplicate, outdated, other
    details: str | None = None
