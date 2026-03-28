from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, JSON, func, Index
from app.db.base import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(String(36), primary_key=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(20), nullable=False, default="mcq")
    options = Column(JSON, nullable=True)
    correct_answer = Column(String(500), nullable=False)
    explanation = Column(Text, nullable=True)
    difficulty = Column(Integer, nullable=False, default=1)
    time_estimate_seconds = Column(Integer, default=30)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_questions_difficulty", "difficulty"),
        Index("ix_questions_type", "question_type"),
    )


class QuestionConcept(Base):
    """Many-to-many: a question can test multiple concepts."""
    __tablename__ = "question_concepts"

    question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True)
    concept_id = Column(String(36), ForeignKey("concepts.id", ondelete="CASCADE"), primary_key=True)

    __table_args__ = (
        Index("ix_qc_concept", "concept_id"),
        Index("ix_qc_question", "question_id"),
    )


class QuestionReport(Base):
    """User-submitted reports for incorrect or problematic questions."""
    __tablename__ = "question_reports"

    id = Column(String(36), primary_key=True)
    question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reason = Column(String(50), nullable=False)  # wrong_answer, unclear, duplicate, outdated, other
    details = Column(Text, nullable=True)
    status = Column(String(20), default="pending")  # pending, reviewed, fixed, dismissed
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_qr_question", "question_id"),
        Index("ix_qr_status", "status"),
    )
