"""
Mastery Tracker — Tracks and updates user progress per concept.

Responsibilities:
  - Update confidence after each answer
  - Update spaced repetition params
  - Derive mastery level
  - Calculate XP earned
  - Detect level-ups and trigger lesson cards
"""

import json
import uuid
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.progress import UserConceptProgress, UserQuestionAttempt, UserDailyStats
from app.models.question import Question
from app.models.concept import Concept
from app.models.user import User
from app.services.spaced_repetition import calculate_next_review, calculate_confidence, get_mastery_level


# XP rewards per difficulty
XP_TABLE = {1: 10, 2: 20, 3: 35}
XP_STREAK_BONUS = 5  # per streak count, capped
DAILY_GOAL = 10  # questions per day

# Level thresholds (same as badges.py)
_LEVELS = [0, 100, 300, 600, 1000, 1800, 3000, 5000, 8000, 12000]


def _xp_level(xp: int) -> int:
    level = 1
    for threshold in _LEVELS:
        if xp >= threshold:
            level = _LEVELS.index(threshold) + 1
    return level


class MasteryTracker:

    def __init__(self, db: Session, user_id: str):
        self.db = db
        self.user_id = user_id

    def process_answer(
        self,
        question: Question,
        concept_id: str,
        selected_answer: str,
        is_correct: bool,
        response_time_ms: int,
    ) -> dict:
        """
        Process a user's answer: update progress, SR params, mastery, XP, streaks.
        Returns a result dict for the API response.
        """
        try:
            return self._process_answer_inner(
                question, concept_id, selected_answer, is_correct, response_time_ms
            )
        except Exception:
            self.db.rollback()
            raise

    def _process_answer_inner(
        self,
        question,
        concept_id: str,
        selected_answer: str,
        is_correct: bool,
        response_time_ms: int,
    ) -> dict:
        # Get or create concept progress
        progress = self._get_or_create_progress(concept_id)

        # Update core metrics
        progress.exposure_count += 1
        if is_correct:
            progress.correct_count += 1
            progress.correct_streak += 1
            progress.error_streak = 0
        else:
            progress.incorrect_count += 1
            progress.error_streak += 1
            progress.correct_streak = 0

        # Update response time (rolling average)
        if progress.avg_response_time_ms == 0:
            progress.avg_response_time_ms = response_time_ms
        else:
            progress.avg_response_time_ms = int(
                0.7 * progress.avg_response_time_ms + 0.3 * response_time_ms
            )

        # Update confidence score
        time_estimate_ms = (question.time_estimate_seconds or 30) * 1000
        progress.confidence_score = calculate_confidence(
            current_confidence=progress.confidence_score,
            is_correct=is_correct,
            response_time_ms=response_time_ms,
            time_estimate_ms=time_estimate_ms,
            exposure_count=progress.exposure_count,
        )

        # Update spaced repetition
        sr_result = calculate_next_review(
            is_correct=is_correct,
            current_ease=progress.ease_factor,
            current_interval=progress.interval_days,
            repetition_number=progress.repetition_number,
            response_time_ms=response_time_ms,
            time_estimate_ms=time_estimate_ms,
            error_streak=progress.error_streak,
        )
        progress.ease_factor = sr_result["ease_factor"]
        progress.interval_days = sr_result["interval_days"]
        progress.repetition_number = sr_result["repetition_number"]
        progress.next_review_at = sr_result["next_review_at"]
        progress.last_seen_at = datetime.utcnow()

        # Update mastery level
        total = progress.correct_count + progress.incorrect_count
        progress.mastery_level = get_mastery_level(
            progress.confidence_score, progress.exposure_count,
            progress.correct_count, total,
        )

        # Calculate XP (with decay for repeated questions and mastery cap)
        # Must be calculated BEFORE adding attempt to session to avoid off-by-one
        xp = self._calculate_xp(
            question.difficulty, is_correct, progress.correct_streak,
            mastery_level=progress.mastery_level,
            question_id=question.id,
        )

        # Record attempt
        attempt = UserQuestionAttempt(
            id=str(uuid.uuid4()),
            user_id=self.user_id,
            question_id=question.id,
            concept_id=concept_id,
            selected_answer=selected_answer,
            is_correct=is_correct,
            response_time_ms=response_time_ms,
            difficulty_at_time=question.difficulty,
        )
        self.db.add(attempt)

        # Store XP on the attempt for per-subject tracking
        attempt.xp_earned = xp

        # Detect level-up before adding XP
        old_xp = (self.db.query(User).filter(User.id == self.user_id).first()).total_xp or 0
        old_level = _xp_level(old_xp)

        # Update daily stats & streaks
        self._update_daily_stats(is_correct, response_time_ms, xp)
        streak_info = self._update_user_streak(xp)

        new_level = _xp_level(old_xp + xp)
        level_up = new_level > old_level

        # Build lesson card if wrong answer
        lesson_card = None
        if not is_correct:
            concept = self.db.query(Concept).filter(Concept.id == concept_id).first()
            if concept and concept.explanation:
                kp = concept.key_points or []
                if isinstance(kp, str):
                    try:
                        kp = json.loads(kp)
                    except (json.JSONDecodeError, TypeError):
                        kp = []
                lesson_card = {
                    "title": f"Let's review: {concept.name}",
                    "content": concept.explanation,
                    "key_points": kp,
                    "type": "mistake_fix",
                }

        # Commit
        self.db.commit()

        # Build review message + cooldown for wrong answers
        cooldown_seconds = None
        if is_correct:
            days = sr_result["interval_days"]
            if days == 0:
                review_msg = "Great! We'll revisit this soon."
            elif days == 1:
                review_msg = "See you tomorrow for review!"
            else:
                review_msg = f"Next review in {days} days."
        else:
            # Calculate cooldown for this wrong question
            wrong_count = progress.error_streak
            cooldown_min = min(
                5 * (1.5 ** (wrong_count - 1)),  # 5, 7.5, 11, 17, 25... minutes
                120  # cap at 2 hours
            )
            cooldown_seconds = int(cooldown_min * 60)
            mins = int(cooldown_min)
            if mins < 1:
                review_msg = "This question will respawn in a few seconds."
            elif mins == 1:
                review_msg = "This question will respawn in 1 minute."
            else:
                review_msg = f"This question will respawn in {mins} minutes."

        # Resolve correct answer text from options
        correct_answer_text = question.correct_answer
        try:
            opts = question.options
            if isinstance(opts, str):
                opts = json.loads(opts)
            if isinstance(opts, dict):
                correct_answer_text = opts.get(question.correct_answer, question.correct_answer)
        except (json.JSONDecodeError, TypeError):
            pass

        return {
            "is_correct": is_correct,
            "correct_answer": question.correct_answer,
            "correct_answer_text": correct_answer_text,
            "explanation": question.explanation,
            "xp_earned": xp,
            "confidence_change": round(progress.confidence_score, 4),
            "mastery_level": progress.mastery_level,
            "streak_count": streak_info["current_streak"],
            "next_review_message": review_msg,
            "level_up": level_up,
            "new_badges": [],
            "lesson_card": lesson_card,
            "cooldown_seconds": cooldown_seconds,
        }

    def _get_or_create_progress(self, concept_id: str) -> UserConceptProgress:
        progress = (
            self.db.query(UserConceptProgress)
            .filter(
                UserConceptProgress.user_id == self.user_id,
                UserConceptProgress.concept_id == concept_id,
            )
            .first()
        )
        if not progress:
            progress = UserConceptProgress(
                id=str(uuid.uuid4()),
                user_id=self.user_id,
                concept_id=concept_id,
            )
            self.db.add(progress)
            self.db.flush()
        return progress

    def _calculate_xp(
        self,
        difficulty: int,
        is_correct: bool,
        correct_streak: int,
        mastery_level: str = "novice",
        question_id: str | None = None,
    ) -> int:
        if not is_correct:
            return 2  # Small consolation XP for trying

        # No XP once concept is mastered
        if mastery_level == "mastered":
            return 0

        base = XP_TABLE.get(difficulty, 10)
        streak_bonus = min(correct_streak, 10) * XP_STREAK_BONUS
        full_xp = base + streak_bonus

        # Diminishing returns for repeated correct answers on same question
        if question_id:
            prior_correct = (
                self.db.query(UserQuestionAttempt)
                .filter(
                    UserQuestionAttempt.user_id == self.user_id,
                    UserQuestionAttempt.question_id == question_id,
                    UserQuestionAttempt.is_correct == True,
                )
                .count()
            )
            if prior_correct >= 4:
                return 0  # No XP after 4th correct answer
            elif prior_correct >= 1:
                # Decay: 100% → 60% → 30% → 10%
                decay = [1.0, 0.6, 0.3, 0.1][min(prior_correct, 3)]
                full_xp = max(1, int(full_xp * decay))

        return full_xp

    def _update_daily_stats(self, is_correct: bool, response_time_ms: int, xp: int):
        today = datetime.utcnow().date()
        stats = (
            self.db.query(UserDailyStats)
            .filter(
                UserDailyStats.user_id == self.user_id,
                UserDailyStats.date == today,
            )
            .first()
        )
        if not stats:
            stats = UserDailyStats(
                id=str(uuid.uuid4()),
                user_id=self.user_id,
                date=today,
                questions_answered=0,
                correct_count=0,
                time_spent_seconds=0,
                xp_earned=0,
            )
            self.db.add(stats)
            self.db.flush()

        stats.questions_answered = (stats.questions_answered or 0) + 1
        if is_correct:
            stats.correct_count = (stats.correct_count or 0) + 1
        stats.time_spent_seconds = (stats.time_spent_seconds or 0) + response_time_ms // 1000
        stats.xp_earned = (stats.xp_earned or 0) + xp

    def _update_user_streak(self, xp: int) -> dict:
        user = self.db.query(User).filter(User.id == self.user_id).first()
        user.total_xp = (user.total_xp or 0) + xp

        today = datetime.utcnow().date()
        yesterday = today - __import__("datetime").timedelta(days=1)

        # Check if already active today
        today_stats = (
            self.db.query(UserDailyStats)
            .filter(UserDailyStats.user_id == self.user_id, UserDailyStats.date == today)
            .first()
        )

        if today_stats and today_stats.questions_answered >= DAILY_GOAL:
            # Check yesterday for streak continuity
            yesterday_stats = (
                self.db.query(UserDailyStats)
                .filter(UserDailyStats.user_id == self.user_id, UserDailyStats.date == yesterday)
                .first()
            )
            if yesterday_stats and yesterday_stats.questions_answered >= DAILY_GOAL:
                if today_stats.streak_day == 0:
                    user.current_streak += 1
                    today_stats.streak_day = user.current_streak
            else:
                # Yesterday missed or didn't meet goal — reset streak to 1
                if today_stats.streak_day == 0:
                    user.current_streak = 1
                    today_stats.streak_day = 1

            user.longest_streak = max(user.longest_streak, user.current_streak)

        return {
            "current_streak": user.current_streak,
            "longest_streak": user.longest_streak,
        }
