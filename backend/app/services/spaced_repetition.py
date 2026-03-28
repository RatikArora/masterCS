"""
Spaced Repetition Service — SM-2 Algorithm Variant

This is the memory engine. It decides WHEN a concept should be revisited.

Key improvements over vanilla SM-2:
  - Response time factors into ease adjustment
  - Error streaks trigger aggressive review
  - Confidence decay over time
"""

from datetime import datetime, timedelta
from app.core.constants import SPACED_INTERVALS, DEFAULT_EASE_FACTOR, MIN_EASE_FACTOR


def calculate_next_review(
    is_correct: bool,
    current_ease: float,
    current_interval: int,
    repetition_number: int,
    response_time_ms: int,
    time_estimate_ms: int,
    error_streak: int,
) -> dict:
    """
    Calculate next review date and updated SM-2 parameters.

    Returns dict with: ease_factor, interval_days, repetition_number, next_review_at
    """
    ease = current_ease
    speed_ratio = response_time_ms / max(time_estimate_ms, 1)

    if is_correct:
        # Correct answer — grow interval
        if repetition_number == 0:
            interval = 1
        elif repetition_number == 1:
            interval = 3
        else:
            interval = int(current_interval * ease)

        repetition_number += 1

        # Adjust ease based on response speed
        if speed_ratio < 0.5:
            # Very fast — strong knowledge
            ease += 0.15
        elif speed_ratio < 1.0:
            # Normal speed
            ease += 0.05
        elif speed_ratio < 2.0:
            # Slow but correct — shaky knowledge
            ease -= 0.05
        else:
            # Very slow — barely knew it
            ease -= 0.10
    else:
        # Incorrect — reset progress partially
        if error_streak >= 3:
            # Repeated failures — aggressive reset
            interval = 0  # review immediately (next session)
            repetition_number = 0
            ease -= 0.3
        elif error_streak >= 1:
            interval = 1
            repetition_number = max(0, repetition_number - 2)
            ease -= 0.2
        else:
            interval = 1
            repetition_number = max(0, repetition_number - 1)
            ease -= 0.1

    # Clamp ease factor
    ease = max(MIN_EASE_FACTOR, min(3.0, ease))

    # Cap interval at max
    max_interval = SPACED_INTERVALS[-1] if SPACED_INTERVALS else 120
    interval = min(interval, max_interval)

    next_review = datetime.utcnow() + timedelta(days=interval)

    return {
        "ease_factor": round(ease, 2),
        "interval_days": interval,
        "repetition_number": repetition_number,
        "next_review_at": next_review,
    }


def calculate_confidence(
    current_confidence: float,
    is_correct: bool,
    response_time_ms: int,
    time_estimate_ms: int,
    exposure_count: int,
) -> float:
    """
    Calculate updated confidence score (0.0 – 1.0).
    Uses exponential moving average with speed bonus/penalty.
    """
    # Base score for this attempt
    if is_correct:
        speed_ratio = response_time_ms / max(time_estimate_ms, 1)
        if speed_ratio < 0.5:
            attempt_score = 1.0
        elif speed_ratio < 1.0:
            attempt_score = 0.9
        elif speed_ratio < 2.0:
            attempt_score = 0.75
        else:
            attempt_score = 0.6
    else:
        attempt_score = 0.0

    # EMA weight — early exposures have more impact
    alpha = max(0.2, 1.0 / (1 + exposure_count * 0.3))

    new_confidence = alpha * attempt_score + (1 - alpha) * current_confidence
    return round(min(1.0, max(0.0, new_confidence)), 4)


def get_mastery_level(confidence: float, exposure_count: int, correct_count: int, total_count: int) -> str:
    """Derive mastery level from confidence + exposure metrics."""
    if exposure_count == 0:
        return "novice"

    accuracy = correct_count / max(total_count, 1)

    # Need both confidence AND accuracy for higher levels
    combined = (confidence * 0.6) + (accuracy * 0.4)

    if combined >= 0.90 and exposure_count >= 8:
        return "mastered"
    elif combined >= 0.75 and exposure_count >= 5:
        return "proficient"
    elif combined >= 0.50 and exposure_count >= 3:
        return "familiar"
    elif exposure_count >= 1:
        return "learning"
    return "novice"
