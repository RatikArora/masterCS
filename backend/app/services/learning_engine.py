"""
Learning Engine — Top-level orchestrator.

Coordinates question selection, answer processing, and progress retrieval.
This is the single entry point for the learning flow API.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.question import Question, QuestionConcept
from app.models.progress import UserConceptProgress, UserQuestionAttempt, UserDailyStats
from app.models.concept import Concept
from app.models.subject import Topic, Subject
from app.services.question_selector import QuestionSelector
from app.services.mastery_tracker import MasteryTracker
from app.schemas.question import (
    QuestionResponse, AnswerSubmit, AnswerResult,
    LearningSession, SessionStats, ConceptProgressBrief,
)
from datetime import datetime


class LearningEngine:

    def __init__(self, db: Session, user_id: str):
        self.db = db
        self.user_id = user_id
        self.selector = QuestionSelector(db, user_id, subject_id="", concept_id=None, topic_id=None)
        self.tracker = MasteryTracker(db, user_id)

    def get_next_question(self, subject_id: str, concept_id: str | None = None, topic_id: str | None = None) -> LearningSession | None:
        """Get the next adaptive question for the user. Optionally scoped to a concept or topic."""
        self.selector.subject_id = subject_id
        self.selector.concept_id = concept_id
        self.selector.topic_id = topic_id

        result = self.selector.select_next()
        if not result:
            return None

        q = result["question"]
        concept_id = result["concept_id"]

        # Get attempt count for this question
        attempt_count = (
            self.db.query(func.count(UserQuestionAttempt.id))
            .filter(
                UserQuestionAttempt.user_id == self.user_id,
                UserQuestionAttempt.question_id == q.id,
            )
            .scalar()
        ) or 0

        # Get session stats
        today = datetime.utcnow().date()
        daily = (
            self.db.query(UserDailyStats)
            .filter(UserDailyStats.user_id == self.user_id, UserDailyStats.date == today)
            .first()
        )

        from app.models.user import User
        user = self.db.query(User).filter(User.id == self.user_id).first()

        # Get concept progress
        progress = (
            self.db.query(UserConceptProgress)
            .filter(
                UserConceptProgress.user_id == self.user_id,
                UserConceptProgress.concept_id == concept_id,
            )
            .first()
        )

        question_resp = QuestionResponse(
            id=q.id,
            question_text=q.question_text,
            question_type=q.question_type,
            options=q.options,
            difficulty=q.difficulty,
            concept_id=concept_id,
            concept_name=result["concept_name"],
            topic_name=result["topic_name"],
            time_estimate_seconds=q.time_estimate_seconds or 30,
            attempt_number=attempt_count,
        )

        session_stats = SessionStats(
            questions_answered_today=daily.questions_answered if daily else 0,
            correct_today=daily.correct_count if daily else 0,
            current_streak=user.current_streak if user else 0,
            xp_today=daily.xp_earned if daily else 0,
        )

        concept_brief = ConceptProgressBrief(
            concept_id=concept_id,
            concept_name=result["concept_name"],
            mastery_level=progress.mastery_level if progress else "novice",
            confidence_score=progress.confidence_score if progress else 0.0,
            exposure_count=progress.exposure_count if progress else 0,
        )

        return LearningSession(
            question=question_resp,
            session_stats=session_stats,
            concept_progress=concept_brief,
        )

    def submit_answer(self, answer: AnswerSubmit) -> AnswerResult:
        """Process a submitted answer and return results."""
        question = self.db.query(Question).filter(Question.id == answer.question_id).first()
        if not question:
            raise ValueError("Question not found")

        # Determine concept (use first linked concept)
        qc = (
            self.db.query(QuestionConcept)
            .filter(QuestionConcept.question_id == question.id)
            .first()
        )
        concept_id = qc.concept_id if qc else None

        is_correct = answer.selected_answer.strip().lower() == question.correct_answer.strip().lower()

        result = self.tracker.process_answer(
            question=question,
            concept_id=concept_id,
            selected_answer=answer.selected_answer,
            is_correct=is_correct,
            response_time_ms=answer.response_time_ms,
        )

        return AnswerResult(**result)
