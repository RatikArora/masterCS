"""
Question Selector — The Brain of Adaptive Difficulty

Decides which question to show next based on:
  1. User's weak areas (push harder on failures)
  2. Spaced repetition schedule (concepts due for review)
  3. New concept progression (follow curriculum order)
  4. Cooldown (never repeat same question too soon)
  5. Difficulty adaptation (rolling accuracy drives difficulty)
"""

import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, not_

from app.models.question import Question, QuestionConcept
from app.models.concept import Concept
from app.models.subject import Topic
from app.models.progress import UserConceptProgress, UserQuestionAttempt
from app.config import get_settings

settings = get_settings()


class QuestionSelector:

    def __init__(self, db: Session, user_id: str, subject_id: str, concept_id: str | None = None, topic_id: str | None = None):
        self.db = db
        self.user_id = user_id
        self.subject_id = subject_id
        self.concept_id = concept_id
        self.topic_id = topic_id

    def select_next(self) -> dict | None:
        """
        Select the next question using weighted category mixing.
        If concept_id is set, only picks questions from that concept.
        Returns dict with question + concept info, or None if no questions available.
        """
        # Concept-focused mode: bypass all adaptive logic
        if self.concept_id:
            return self._get_concept_focused_question()

        roll = random.random()

        # First priority: previously wrong questions
        if roll < 0.20:
            result = self._get_previously_wrong_question()
            if result:
                return result

        if roll < 0.20 + settings.WEAK_QUESTION_RATIO:
            result = self._get_weak_area_question()
            if result:
                return result

        if roll < 0.20 + settings.WEAK_QUESTION_RATIO + settings.REVISION_QUESTION_RATIO:
            result = self._get_revision_question()
            if result:
                return result

        # Default: new concept question
        result = self._get_new_concept_question()
        if result:
            return result

        # Fallback chain: try other categories
        return (
            self._get_previously_wrong_question()
            or self._get_revision_question()
            or self._get_weak_area_question()
            or self._get_any_available_question()
        )

    def _get_recently_answered_ids(self) -> list[str]:
        """Get question IDs answered within cooldown period."""
        cooldown_cutoff = datetime.utcnow() - timedelta(hours=settings.QUESTION_COOLDOWN_HOURS)
        rows = (
            self.db.query(UserQuestionAttempt.question_id)
            .filter(
                UserQuestionAttempt.user_id == self.user_id,
                UserQuestionAttempt.attempted_at > cooldown_cutoff,
            )
            .all()
        )
        return [r[0] for r in rows]

    def _get_correctly_answered_ids(self, concept_ids: list[str] | None = None) -> set[str]:
        """Get question IDs that the user has already answered correctly.
        These are permanently excluded — no need to repeat mastered questions."""
        query = (
            self.db.query(UserQuestionAttempt.question_id)
            .filter(
                UserQuestionAttempt.user_id == self.user_id,
                UserQuestionAttempt.is_correct == True,
            )
        )
        if concept_ids:
            query = query.filter(UserQuestionAttempt.concept_id.in_(concept_ids))
        return {r[0] for r in query.distinct().all()}

    def _get_concept_focused_question(self) -> dict | None:
        """Select a question specifically for the focused concept, with adaptive difficulty."""
        if not self.concept_id:
            return None

        recently_answered = self._get_recently_answered_ids()
        correctly_answered = self._get_correctly_answered_ids([self.concept_id])
        target_diff = self._get_target_difficulty()

        # Exclude both recently answered and correctly mastered questions
        exclude_ids = set(recently_answered) | correctly_answered

        query = (
            self.db.query(Question)
            .join(QuestionConcept, Question.id == QuestionConcept.question_id)
            .filter(QuestionConcept.concept_id == self.concept_id)
        )

        if exclude_ids:
            query = query.filter(not_(Question.id.in_(exclude_ids)))

        questions = query.all()
        if not questions:
            # If all questions mastered, allow correctly answered but still exclude cooldown
            query = (
                self.db.query(Question)
                .join(QuestionConcept, Question.id == QuestionConcept.question_id)
                .filter(QuestionConcept.concept_id == self.concept_id)
            )
            if recently_answered:
                query = query.filter(not_(Question.id.in_(recently_answered)))
            questions = query.all()

        if not questions:
            return None

        # Prefer questions near target difficulty
        scored = sorted(questions, key=lambda q: abs(q.difficulty - target_diff))
        top = scored[: min(3, len(scored))]
        chosen = random.choice(top)

        return self._build_result(chosen, self.concept_id)

    def _get_previously_wrong_question(self) -> dict | None:
        """Select a question the user previously answered incorrectly for review."""
        concept_ids = self._get_subject_concept_ids()
        recently_answered = self._get_recently_answered_ids()

        # Find questions answered incorrectly that haven't been answered correctly since
        wrong_qids = (
            self.db.query(UserQuestionAttempt.question_id)
            .filter(
                UserQuestionAttempt.user_id == self.user_id,
                UserQuestionAttempt.is_correct == False,
                UserQuestionAttempt.concept_id.in_(concept_ids),
            )
            .distinct()
            .all()
        )
        wrong_ids = [r[0] for r in wrong_qids]

        if not wrong_ids:
            return None

        # Exclude questions answered correctly in a later attempt
        correct_qids = (
            self.db.query(UserQuestionAttempt.question_id)
            .filter(
                UserQuestionAttempt.user_id == self.user_id,
                UserQuestionAttempt.is_correct == True,
                UserQuestionAttempt.question_id.in_(wrong_ids),
            )
            .distinct()
            .all()
        )
        correct_set = {r[0] for r in correct_qids}

        # Keep only questions still not answered correctly
        still_wrong = [qid for qid in wrong_ids if qid not in correct_set]

        # Also exclude recently answered (cooldown)
        if recently_answered:
            still_wrong = [qid for qid in still_wrong if qid not in recently_answered]

        if not still_wrong:
            return None

        qid = random.choice(still_wrong)
        question = self.db.query(Question).filter(Question.id == qid).first()
        if not question:
            return None

        qc = self.db.query(QuestionConcept).filter(QuestionConcept.question_id == qid).first()
        concept_id = qc.concept_id if qc else ""

        return self._build_result(question, concept_id)

    def _get_target_difficulty(self) -> int:
        """Calculate target difficulty from recent accuracy (last 20 answers)."""
        recent = (
            self.db.query(UserQuestionAttempt)
            .filter(UserQuestionAttempt.user_id == self.user_id)
            .order_by(UserQuestionAttempt.attempted_at.desc())
            .limit(20)
            .all()
        )
        if not recent:
            return 1  # Start easy

        accuracy = sum(1 for a in recent if a.is_correct) / len(recent)

        if accuracy >= 0.8:
            return 3  # Hard
        elif accuracy >= 0.5:
            return 2  # Medium
        return 1  # Easy

    def _get_subject_concept_ids(self) -> list[str]:
        """Get concept IDs scoped to subject, or topic if set."""
        query = (
            self.db.query(Concept.id)
            .join(Topic, Concept.topic_id == Topic.id)
        )
        if self.topic_id:
            query = query.filter(Topic.id == self.topic_id)
        else:
            query = query.filter(Topic.subject_id == self.subject_id)
        return [r[0] for r in query.all()]

    def _get_weak_area_question(self) -> dict | None:
        """Select a question from user's weakest concepts."""
        concept_ids = self._get_subject_concept_ids()
        recently_answered = self._get_recently_answered_ids()

        # Find weakest concepts: low confidence OR high error streak
        weak_progresses = (
            self.db.query(UserConceptProgress)
            .filter(
                UserConceptProgress.user_id == self.user_id,
                UserConceptProgress.concept_id.in_(concept_ids),
                or_(
                    UserConceptProgress.confidence_score < 0.4,
                    UserConceptProgress.error_streak >= 2,
                ),
            )
            .order_by(UserConceptProgress.confidence_score.asc())
            .limit(5)
            .all()
        )

        if not weak_progresses:
            return None

        # Pick a random weak concept (slight randomization keeps it fresh)
        weak = random.choice(weak_progresses)

        return self._pick_question_for_concept(weak.concept_id, recently_answered)

    def _get_revision_question(self) -> dict | None:
        """Select a question from concepts due for spaced repetition review."""
        concept_ids = self._get_subject_concept_ids()
        recently_answered = self._get_recently_answered_ids()
        now = datetime.utcnow()

        # Concepts due for review
        due_progresses = (
            self.db.query(UserConceptProgress)
            .filter(
                UserConceptProgress.user_id == self.user_id,
                UserConceptProgress.concept_id.in_(concept_ids),
                UserConceptProgress.next_review_at <= now,
                UserConceptProgress.exposure_count > 0,
            )
            .order_by(UserConceptProgress.next_review_at.asc())
            .limit(5)
            .all()
        )

        if not due_progresses:
            return None

        due = random.choice(due_progresses)
        return self._pick_question_for_concept(due.concept_id, recently_answered)

    def _get_new_concept_question(self) -> dict | None:
        """Select a question from the next unseen/least-explored concept."""
        concept_ids = self._get_subject_concept_ids()
        recently_answered = self._get_recently_answered_ids()

        explored = (
            self.db.query(UserConceptProgress.concept_id)
            .filter(
                UserConceptProgress.user_id == self.user_id,
                UserConceptProgress.concept_id.in_(concept_ids),
                UserConceptProgress.exposure_count >= 3,
            )
            .all()
        )
        explored_ids = {r[0] for r in explored}

        # Get next concept in order that hasn't been sufficiently explored
        query = (
            self.db.query(Concept)
            .join(Topic, Concept.topic_id == Topic.id)
        )
        if self.topic_id:
            query = query.filter(Topic.id == self.topic_id)
        else:
            query = query.filter(Topic.subject_id == self.subject_id)

        if explored_ids:
            query = query.filter(not_(Concept.id.in_(explored_ids)))

        next_concept = query.order_by(Topic.order_index, Concept.order_index).first()

        if not next_concept:
            return None

        return self._pick_question_for_concept(next_concept.id, recently_answered)

    def _get_any_available_question(self) -> dict | None:
        """Last resort: get any question not correctly answered or recently seen."""
        recently_answered = self._get_recently_answered_ids()
        concept_ids = self._get_subject_concept_ids()
        correctly_answered = self._get_correctly_answered_ids(concept_ids)
        exclude_ids = set(recently_answered) | correctly_answered

        query = (
            self.db.query(Question, QuestionConcept.concept_id)
            .join(QuestionConcept, Question.id == QuestionConcept.question_id)
            .filter(QuestionConcept.concept_id.in_(concept_ids))
        )

        if exclude_ids:
            query = query.filter(not_(Question.id.in_(exclude_ids)))

        questions = query.all()
        if not questions:
            return None

        q, concept_id = random.choice(questions)
        return self._build_result(q, concept_id)

    def _pick_question_for_concept(self, concept_id: str, recently_answered: list[str]) -> dict | None:
        """Pick the best question for a given concept, excluding mastered questions."""
        target_diff = self._get_target_difficulty()
        correctly_answered = self._get_correctly_answered_ids([concept_id])
        exclude_ids = set(recently_answered) | correctly_answered

        query = (
            self.db.query(Question)
            .join(QuestionConcept, Question.id == QuestionConcept.question_id)
            .filter(QuestionConcept.concept_id == concept_id)
        )

        if exclude_ids:
            query = query.filter(not_(Question.id.in_(exclude_ids)))

        questions = query.all()
        if not questions:
            return None

        # Prefer questions near target difficulty
        scored = []
        for q in questions:
            diff_delta = abs(q.difficulty - target_diff)
            scored.append((q, diff_delta))

        scored.sort(key=lambda x: x[1])

        # Take from top 3 closest matches, pick randomly
        top = scored[: min(3, len(scored))]
        chosen = random.choice(top)[0]

        return self._build_result(chosen, concept_id)

    def _build_result(self, question: Question, concept_id: str) -> dict:
        """Build the response dict with question + context."""
        concept = self.db.query(Concept).filter(Concept.id == concept_id).first()
        topic = self.db.query(Topic).filter(Topic.id == concept.topic_id).first() if concept else None

        return {
            "question": question,
            "concept_id": concept_id,
            "concept_name": concept.name if concept else "",
            "topic_name": topic.name if topic else "",
        }
