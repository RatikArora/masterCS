"""
Question Selector v3 — Advanced Multi-Factor Scoring Engine

Every candidate question gets a priority score based on 10 factors:

  Core learning signals:
    1. Wrong-answer urgency   — previously-wrong questions return after cooldown
    2. Concept weakness       — low confidence / high error streak concepts
    3. Spaced repetition      — overdue concepts with forgetting curve prediction
    4. Novelty                — unexplored concepts need introduction
    5. Difficulty match       — questions near user's adaptive difficulty level

  Session intelligence:
    6. Response time signal   — slow correct = shaky knowledge, boosts concept
    7. Session diversity      — penalizes repeating same concept/topic in a session
    8. Performance momentum   — hot streaks push harder, struggles ease off
    9. Mastery proximity      — concepts close to leveling up get a motivational boost
   10. Recency penalty        — gentle penalty for recently seen questions

Selection: top-scored questions with weighted randomization.
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

# Core learning signals
WEIGHT_WRONG_ANSWER = 50.0         # massive boost for previously-wrong questions
WEIGHT_WRONG_REPEAT = 8.0          # extra per additional wrong attempt
WEIGHT_CONCEPT_WEAKNESS = 15.0     # low confidence concepts
WEIGHT_ERROR_STREAK = 12.0         # per consecutive error on concept
WEIGHT_SR_OVERDUE = 20.0           # spaced repetition overdue
WEIGHT_NOVELTY = 10.0              # unseen concepts
WEIGHT_DIFFICULTY_MATCH = 5.0      # bonus for matching target difficulty
RECENCY_PENALTY_PER_HOUR = 2.0     # gentle penalty for recently seen (not blocking)

# Session intelligence
WEIGHT_SLOW_CORRECT = 8.0          # boost for concepts where user answered slowly-but-correct
WEIGHT_SESSION_DIVERSITY = -6.0    # penalty for repeating same concept within session
WEIGHT_TOPIC_DIVERSITY = -3.0      # penalty for repeating same topic within session
WEIGHT_MOMENTUM_BOOST = 3.0        # difficulty bump when user is on a streak
WEIGHT_MASTERY_PROXIMITY = 7.0     # boost for concepts close to leveling up

# Cooldown for wrong answers (game-style "respawn" timer)
WRONG_COOLDOWN_MINUTES_BASE = 5    # 5 min after 1st wrong
WRONG_COOLDOWN_SCALE = 1.5         # multiplier per additional wrong attempt
WRONG_COOLDOWN_MAX_MINUTES = 120   # cap at 2 hours

# Mastery level thresholds (confidence needed for each level)
_MASTERY_THRESHOLDS = {
    "novice": 0.0,
    "learning": 0.25,
    "familiar": 0.50,
    "proficient": 0.75,
    "mastered": 0.90,
}
_MASTERY_ORDER = ["novice", "learning", "familiar", "proficient", "mastered"]


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
        self._on_cooldown: dict[str, datetime] | None = None  # question_id → cooldown_expires_at
        # v3: Session intelligence
        self._slow_correct_concepts: dict[str, float] | None = None  # concept_id → slowness_ratio
        self._session_concept_counts: dict[str, int] | None = None   # concept_id → times shown today
        self._session_topic_counts: dict[str, int] | None = None     # topic_id → times shown today
        self._recent_momentum: float = 0.0  # -1.0 (struggling) to +1.0 (hot streak)
        self._concept_to_topic: dict[str, str] = {}  # concept_id → topic_id mapping

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
            score, reasons = self._score_question_with_reasons(question, q_concept_id)
            scored.append((question, q_concept_id, score, reasons))

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
        chosen_q, chosen_cid, chosen_reasons = top[0][0], top[0][1], top[0][3]
        for q, cid, sc, reasons in top:
            cumulative += max(sc, 0.1)
            if r <= cumulative:
                chosen_q, chosen_cid, chosen_reasons = q, cid, reasons
                break

        return self._build_result(chosen_q, chosen_cid, chosen_reasons)

    # ── Data preloading (bulk queries — no N+1) ─────────────────────

    def _preload_user_data(self, concept_ids: list[str]):
        """Load all user progress data in bulk for scoring."""
        now = datetime.utcnow()

        # Last question the user answered — only exclude if it was correct
        last = (
            self.db.query(UserQuestionAttempt.question_id, UserQuestionAttempt.is_correct)
            .filter(UserQuestionAttempt.user_id == self.user_id)
            .order_by(UserQuestionAttempt.attempted_at.desc())
            .first()
        )
        if last and last[1]:
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

        # ── Cooldowns for wrong questions ──
        self._on_cooldown = {}
        if self._wrong_question_map:
            latest_wrong = (
                self.db.query(
                    UserQuestionAttempt.question_id,
                    func.max(UserQuestionAttempt.attempted_at),
                )
                .filter(
                    UserQuestionAttempt.user_id == self.user_id,
                    UserQuestionAttempt.is_correct == False,
                    UserQuestionAttempt.question_id.in_(list(self._wrong_question_map.keys())),
                )
                .group_by(UserQuestionAttempt.question_id)
                .all()
            )
            for qid, last_wrong_at in latest_wrong:
                wrong_count = self._wrong_question_map.get(qid, 1)
                cooldown_min = min(
                    WRONG_COOLDOWN_MINUTES_BASE * (WRONG_COOLDOWN_SCALE ** (wrong_count - 1)),
                    WRONG_COOLDOWN_MAX_MINUTES,
                )
                expires_at = last_wrong_at + timedelta(minutes=cooldown_min)
                if expires_at > now:
                    self._on_cooldown[qid] = expires_at

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

        # ── v3: Session intelligence signals ──

        # Slow-correct concepts: avg response time vs expected time
        # Concepts where user consistently takes >1.5x the expected time are "shaky"
        self._slow_correct_concepts = {}
        for cid, progress in self._concept_progress_map.items():
            if progress.exposure_count > 0 and progress.avg_response_time_ms > 0:
                # Get avg time_estimate for questions in this concept
                avg_estimate = (
                    self.db.query(func.avg(Question.time_estimate_seconds))
                    .join(QuestionConcept, Question.id == QuestionConcept.question_id)
                    .filter(QuestionConcept.concept_id == cid)
                    .scalar()
                ) or 30
                expected_ms = avg_estimate * 1000
                if expected_ms > 0:
                    slowness = progress.avg_response_time_ms / expected_ms
                    if slowness > 1.3:
                        self._slow_correct_concepts[cid] = min(slowness - 1.0, 2.0)

        # Session diversity: concepts and topics shown today
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        session_attempts = (
            self.db.query(
                UserQuestionAttempt.concept_id,
                func.count(UserQuestionAttempt.id),
            )
            .filter(
                UserQuestionAttempt.user_id == self.user_id,
                UserQuestionAttempt.attempted_at >= today_start,
                UserQuestionAttempt.concept_id.in_(concept_ids),
            )
            .group_by(UserQuestionAttempt.concept_id)
            .all()
        )
        self._session_concept_counts = {cid: cnt for cid, cnt in session_attempts}

        # Build concept → topic mapping and aggregate topic counts
        concept_topics = (
            self.db.query(Concept.id, Concept.topic_id)
            .filter(Concept.id.in_(concept_ids))
            .all()
        )
        self._concept_to_topic = {cid: tid for cid, tid in concept_topics}
        self._session_topic_counts = {}
        for cid, cnt in self._session_concept_counts.items():
            tid = self._concept_to_topic.get(cid)
            if tid:
                self._session_topic_counts[tid] = self._session_topic_counts.get(tid, 0) + cnt

        # Performance momentum: recent 10 answers → streak direction
        recent_10 = (
            self.db.query(UserQuestionAttempt.is_correct)
            .filter(UserQuestionAttempt.user_id == self.user_id)
            .order_by(UserQuestionAttempt.attempted_at.desc())
            .limit(10)
            .all()
        )
        if recent_10:
            correct_ratio = sum(1 for r in recent_10 if r[0]) / len(recent_10)
            self._recent_momentum = (correct_ratio - 0.5) * 2  # maps 0-1 → -1 to +1

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

        # Exclude questions currently on cooldown (wrong-answer respawn timer)
        if self._on_cooldown:
            query = query.filter(not_(Question.id.in_(list(self._on_cooldown.keys()))))

        # Exclude mastered questions unless we've run out
        if not allow_mastered and self._correctly_answered:
            query = query.filter(not_(Question.id.in_(self._correctly_answered)))

        return query.all()

    # ── Scoring engine ──────────────────────────────────────────────

    def _score_question_with_reasons(self, question: Question, concept_id: str) -> tuple[float, list[str]]:
        """Score a question and collect human-readable reasons for the selection."""
        score = 0.0
        reasons: list[str] = []
        now = datetime.utcnow()
        progress = self._concept_progress_map.get(concept_id)

        # ── Factor 1: Wrong-answer urgency ──
        wrong_count = self._wrong_question_map.get(question.id, 0)
        if wrong_count > 0:
            score += WEIGHT_WRONG_ANSWER + (wrong_count - 1) * WEIGHT_WRONG_REPEAT
            reasons.append(f"You got this wrong {wrong_count}× — time to master it")

        # ── Factor 2: Concept weakness ──
        if progress:
            weakness = 1.0 - progress.confidence_score
            score += weakness * WEIGHT_CONCEPT_WEAKNESS
            if progress.error_streak > 0:
                score += progress.error_streak * WEIGHT_ERROR_STREAK
            if weakness > 0.5:
                reasons.append("Strengthening a weak concept")

        # ── Factor 3: Spaced repetition overdue (with forgetting curve) ──
        if progress and progress.next_review_at and progress.exposure_count > 0:
            if progress.next_review_at <= now:
                overdue_hours = (now - progress.next_review_at).total_seconds() / 3600
                overdue_factor = min(overdue_hours / 168, 1.0)
                score += WEIGHT_SR_OVERDUE * (0.5 + 0.5 * overdue_factor)
                reasons.append("Due for spaced repetition review")
            else:
                hours_until = (progress.next_review_at - now).total_seconds() / 3600
                if hours_until < 6:
                    approaching_factor = 1.0 - (hours_until / 6)
                    score += WEIGHT_SR_OVERDUE * 0.15 * approaching_factor

        # ── Factor 4: Novelty (unseen concept) ──
        if not progress or progress.exposure_count == 0:
            score += WEIGHT_NOVELTY
            reasons.append("Exploring a new concept")

        # ── Factor 5: Difficulty match (momentum-aware) ──
        target = self._target_diff
        if self._recent_momentum > 0.3:
            target = min(target + 1, 3)
        elif self._recent_momentum < -0.3:
            target = max(target - 1, 1)

        diff_delta = abs(question.difficulty - target)
        if diff_delta == 0:
            score += WEIGHT_DIFFICULTY_MATCH
        elif diff_delta == 1:
            score += WEIGHT_DIFFICULTY_MATCH * 0.3

        # ── Factor 6: Response time signal (slow correct = shaky) ──
        slowness = self._slow_correct_concepts.get(concept_id, 0)
        if slowness > 0:
            score += WEIGHT_SLOW_CORRECT * min(slowness, 1.5)
            if slowness > 0.5:
                reasons.append("You answered slowly last time — reinforcing")

        # ── Factor 7: Session diversity (concept-level) ──
        if not self.concept_id:
            concept_seen = self._session_concept_counts.get(concept_id, 0)
            if concept_seen > 2:
                score += WEIGHT_SESSION_DIVERSITY * min(concept_seen - 2, 4)

        # ── Factor 8: Session diversity (topic-level) ──
        if not self.concept_id and not self.topic_id:
            topic_id = self._concept_to_topic.get(concept_id)
            if topic_id:
                topic_seen = self._session_topic_counts.get(topic_id, 0)
                if topic_seen > 5:
                    score += WEIGHT_TOPIC_DIVERSITY * min(topic_seen - 5, 3)

        # ── Factor 9: Performance momentum ──
        if self._recent_momentum > 0.3:
            if question.difficulty >= 2:
                score += WEIGHT_MOMENTUM_BOOST * self._recent_momentum
                if question.difficulty == 3:
                    reasons.append("You're on fire — leveling up difficulty")
        elif self._recent_momentum < -0.3:
            if question.difficulty <= 2:
                score += WEIGHT_MOMENTUM_BOOST * abs(self._recent_momentum)

        # ── Factor 10: Mastery proximity ──
        if progress and progress.confidence_score > 0:
            current_level_idx = _MASTERY_ORDER.index(progress.mastery_level) if progress.mastery_level in _MASTERY_ORDER else 0
            if current_level_idx < len(_MASTERY_ORDER) - 1:
                next_level = _MASTERY_ORDER[current_level_idx + 1]
                next_threshold = _MASTERY_THRESHOLDS[next_level]
                distance = next_threshold - progress.confidence_score
                if 0 < distance <= 0.15:
                    proximity = 1.0 - (distance / 0.15)
                    score += WEIGHT_MASTERY_PROXIMITY * proximity
                    reasons.append(f"Almost {next_level} — one more push!")

        # ── Factor 11: Recency penalty (gentle) ──
        last_seen = self._attempt_times.get(question.id)
        if last_seen:
            hours_ago = (now - last_seen).total_seconds() / 3600
            if hours_ago < 1:
                score -= RECENCY_PENALTY_PER_HOUR * (1 - hours_ago)

        if not reasons:
            reasons.append("Adaptive selection based on your learning profile")

        return score, reasons

    def _score_question(self, question: Question, concept_id: str) -> float:
        """Compute score only (no reasons) — used for batch scoring."""
        score, _ = self._score_question_with_reasons(question, concept_id)
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

    def _build_result(self, question: Question, concept_id: str, reasons: list[str] | None = None) -> dict:
        """Build the response dict with question + context + selection insights."""
        concept = self.db.query(Concept).filter(Concept.id == concept_id).first()
        topic = self.db.query(Topic).filter(Topic.id == concept.topic_id).first() if concept else None

        # Include cooldown info for the user's current wrong questions
        cooldowns = []
        now = datetime.utcnow()
        for qid, expires_at in (self._on_cooldown or {}).items():
            remaining_sec = int((expires_at - now).total_seconds())
            if remaining_sec > 0:
                cooldowns.append({
                    "question_id": qid,
                    "expires_in_seconds": remaining_sec,
                })

        # Pick the most relevant reason (first one)
        selection_reason = (reasons[0] if reasons else "Adaptive selection based on your learning profile")

        return {
            "question": question,
            "concept_id": concept_id,
            "concept_name": concept.name if concept else "",
            "topic_name": topic.name if topic else "",
            "cooldown_questions": cooldowns,
            "selection_reason": selection_reason,
        }
