"""
Question Selector v2 — Multi-Factor Scoring Engine

Every candidate question gets a priority score based on:
  1. Wrong-answer urgency  — questions the user got wrong MUST come back
  2. Concept weakness      — low confidence / high error streak concepts
  3. Spaced repetition     — concepts overdue for review
  4. Novelty               — unexplored concepts need introduction
  5. Difficulty match      — questions near user's adaptive difficulty level
  6. Recency penalty       — only the LAST question is excluded (no time-based cooldown)

Selection: top-scored questions with slight randomization.
Works identically for normal mode AND concept-focused mode.
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

# ── Scoring weights ─────────────────────────────────────────────────
WEIGHT_WRONG_ANSWER = 50.0      # massive boost for previously-wrong questions
WEIGHT_WRONG_REPEAT = 8.0       # extra per additional wrong attempt
WEIGHT_CONCEPT_WEAKNESS = 15.0  # low confidence concepts
WEIGHT_ERROR_STREAK = 12.0      # per consecutive error on concept
WEIGHT_SR_OVERDUE = 20.0        # spaced repetition overdue
WEIGHT_NOVELTY = 10.0           # unseen concepts
WEIGHT_DIFFICULTY_MATCH = 5.0   # bonus for matching target difficulty
RECENCY_PENALTY_PER_HOUR = 2.0  # gentle penalty for recently seen (not blocking)


class QuestionSelector:

    def __init__(self, db: Session, user_id: str, subject_id: str,
                 concept_id: str | None = None, topic_id: str | None = None):
        self.db = db
        self.user_id = user_id
        self.subject_id = subject_id
        self.concept_id = concept_id
        self.topic_id = topic_id
        # Cache fields populated lazily
        self._target_diff: int | None = None
        self._concept_progress_map: dict[str, UserConceptProgress] | None = None
        self._wrong_question_map: dict[str, int] | None = None
        self._last_question_id: str | None = None
        self._correctly_answered: set[str] | None = None
        self._attempt_times: dict[str, datetime] | None = None

    # ── Public API ──────────────────────────────────────────────────

    def select_next(self) -> dict | None:
        """Score all candidate questions and pick the best one."""
        concept_ids = self._get_subject_concept_ids()
        if not concept_ids:
            return None

        # Pre-load all user data in bulk (efficient — one query each)
        self._preload_user_data(concept_ids)

        # Get all candidate questions
        candidates = self._get_candidate_questions(concept_ids)
        if not candidates:
            # All mastered — allow correctly answered ones (exclude only last Q)
            candidates = self._get_candidate_questions(concept_ids, allow_mastered=True)
        if not candidates:
            return None

        # Score each candidate
        scored = []
        for question, q_concept_id in candidates:
            score = self._score_question(question, q_concept_id)
            scored.append((question, q_concept_id, score))

        # Sort by score descending
        scored.sort(key=lambda x: x[2], reverse=True)

        # Pick from top 5 with weighted randomization (higher score = more likely)
        top_n = min(5, len(scored))
        top = scored[:top_n]

        # Weighted random: use score as weight
        weights = [max(s[2], 0.1) for s in top]
        total_w = sum(weights)
        r = random.random() * total_w
        cumulative = 0.0
        chosen_q, chosen_cid = top[0][0], top[0][1]
        for q, cid, sc in top:
            cumulative += max(sc, 0.1)
            if r <= cumulative:
                chosen_q, chosen_cid = q, cid
                break

        return self._build_result(chosen_q, chosen_cid)

    # ── Data preloading (bulk queries — no N+1) ─────────────────────

    def _preload_user_data(self, concept_ids: list[str]):
        """Load all user progress data in bulk for scoring."""
        # Last question the user answered — only exclude if it was correct
        # If user got it WRONG, we WANT it to come back immediately
        last = (
            self.db.query(UserQuestionAttempt.question_id, UserQuestionAttempt.is_correct)
            .filter(UserQuestionAttempt.user_id == self.user_id)
            .order_by(UserQuestionAttempt.attempted_at.desc())
            .first()
        )
        if last and last[1]:  # Only exclude if last answer was correct
            self._last_question_id = last[0]
        else:
            self._last_question_id = None

        # Correctly answered questions (permanently excluded)
        self._correctly_answered = self._get_correctly_answered_ids(concept_ids)

        # Concept progress map
        progresses = (
            self.db.query(UserConceptProgress)
            .filter(
                UserConceptProgress.user_id == self.user_id,
                UserConceptProgress.concept_id.in_(concept_ids),
            )
            .all()
        )
        self._concept_progress_map = {p.concept_id: p for p in progresses}

        # Wrong question map: question_id → number of wrong attempts (only still-wrong)
        wrong_attempts = (
            self.db.query(
                UserQuestionAttempt.question_id,
                func.count(UserQuestionAttempt.id),
            )
            .filter(
                UserQuestionAttempt.user_id == self.user_id,
                UserQuestionAttempt.is_correct == False,
                UserQuestionAttempt.concept_id.in_(concept_ids),
            )
            .group_by(UserQuestionAttempt.question_id)
            .all()
        )
        self._wrong_question_map = {
            qid: cnt for qid, cnt in wrong_attempts
            if qid not in self._correctly_answered
        }

        # Most recent attempt time per question (for recency penalty)
        recent_attempts = (
            self.db.query(
                UserQuestionAttempt.question_id,
                func.max(UserQuestionAttempt.attempted_at),
            )
            .filter(
                UserQuestionAttempt.user_id == self.user_id,
                UserQuestionAttempt.concept_id.in_(concept_ids),
            )
            .group_by(UserQuestionAttempt.question_id)
            .all()
        )
        self._attempt_times = {qid: t for qid, t in recent_attempts}

        # Target difficulty
        self._target_diff = self._get_target_difficulty()

    # ── Candidate retrieval ─────────────────────────────────────────

    def _get_candidate_questions(self, concept_ids: list[str],
                                  allow_mastered: bool = False) -> list[tuple[Question, str]]:
        """Get all questions in scope, excluding mastered (unless allow_mastered)
        and the last question answered."""
        query = (
            self.db.query(Question, QuestionConcept.concept_id)
            .join(QuestionConcept, Question.id == QuestionConcept.question_id)
        )

        if self.concept_id:
            query = query.filter(QuestionConcept.concept_id == self.concept_id)
        else:
            query = query.filter(QuestionConcept.concept_id.in_(concept_ids))

        # Always exclude the very last question (avoid immediate repeat)
        if self._last_question_id:
            query = query.filter(Question.id != self._last_question_id)

        # Exclude mastered questions unless we've run out
        if not allow_mastered and self._correctly_answered:
            query = query.filter(not_(Question.id.in_(self._correctly_answered)))

        return query.all()

    # ── Scoring engine ──────────────────────────────────────────────

    def _score_question(self, question: Question, concept_id: str) -> float:
        """Compute a priority score for a single question."""
        score = 0.0
        now = datetime.utcnow()
        progress = self._concept_progress_map.get(concept_id)

        # ── Factor 1: Wrong-answer urgency ──
        wrong_count = self._wrong_question_map.get(question.id, 0)
        if wrong_count > 0:
            # Base score for being wrong + escalation per repeat failure
            score += WEIGHT_WRONG_ANSWER + (wrong_count - 1) * WEIGHT_WRONG_REPEAT

        # ── Factor 2: Concept weakness ──
        if progress:
            # Lower confidence → higher score (invert: 1.0 - confidence)
            weakness = 1.0 - progress.confidence_score
            score += weakness * WEIGHT_CONCEPT_WEAKNESS

            # Error streak bonus (each consecutive error adds urgency)
            if progress.error_streak > 0:
                score += progress.error_streak * WEIGHT_ERROR_STREAK

        # ── Factor 3: Spaced repetition overdue ──
        if progress and progress.next_review_at and progress.exposure_count > 0:
            if progress.next_review_at <= now:
                # How overdue (capped at 7 days for scoring)
                overdue_hours = (now - progress.next_review_at).total_seconds() / 3600
                overdue_factor = min(overdue_hours / 168, 1.0)  # cap at 7 days
                score += WEIGHT_SR_OVERDUE * (0.5 + 0.5 * overdue_factor)

        # ── Factor 4: Novelty (unseen concept) ──
        if not progress or progress.exposure_count == 0:
            score += WEIGHT_NOVELTY

        # ── Factor 5: Difficulty match ──
        diff_delta = abs(question.difficulty - self._target_diff)
        if diff_delta == 0:
            score += WEIGHT_DIFFICULTY_MATCH
        elif diff_delta == 1:
            score += WEIGHT_DIFFICULTY_MATCH * 0.3

        # ── Factor 6: Recency penalty (gentle) ──
        last_seen = self._attempt_times.get(question.id)
        if last_seen:
            hours_ago = (now - last_seen).total_seconds() / 3600
            if hours_ago < 1:
                # Seen very recently — penalty (but NOT exclusion)
                score -= RECENCY_PENALTY_PER_HOUR * (1 - hours_ago)

        return score

    # ── Helper methods ──────────────────────────────────────────────

    def _get_correctly_answered_ids(self, concept_ids: list[str] | None = None) -> set[str]:
        """Get question IDs that the user has answered correctly at least once.
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
            return 1

        accuracy = sum(1 for a in recent if a.is_correct) / len(recent)

        if accuracy >= 0.8:
            return 3
        elif accuracy >= 0.5:
            return 2
        return 1

    def _get_subject_concept_ids(self) -> list[str]:
        """Get concept IDs scoped to subject, or topic if set."""
        if self.concept_id:
            return [self.concept_id]

        query = (
            self.db.query(Concept.id)
            .join(Topic, Concept.topic_id == Topic.id)
        )
        if self.topic_id:
            query = query.filter(Topic.id == self.topic_id)
        else:
            query = query.filter(Topic.subject_id == self.subject_id)
        return [r[0] for r in query.all()]

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
