"""Mastery level definitions and learning engine constants."""

from enum import Enum


class MasteryLevel(str, Enum):
    NOVICE = "novice"
    LEARNING = "learning"
    FAMILIAR = "familiar"
    PROFICIENT = "proficient"
    MASTERED = "mastered"


class QuestionType(str, Enum):
    MCQ = "mcq"
    TRUE_FALSE = "true_false"
    FILL_BLANK = "fill_blank"


class Difficulty(int, Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


# SM-2 Spaced Repetition intervals (in days)
SPACED_INTERVALS = [1, 3, 7, 14, 30, 60, 120]

# Default ease factor
DEFAULT_EASE_FACTOR = 2.5
MIN_EASE_FACTOR = 1.3

# Mastery calculation weights
WEIGHT_ACCURACY = 0.5
WEIGHT_CONSISTENCY = 0.3
WEIGHT_RECENCY = 0.2
