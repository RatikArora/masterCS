"""Learning flow routes — the core interactive endpoints."""

import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.question import Question, QuestionConcept, QuestionReport
from app.models.concept import Concept
from app.models.subject import Topic
from app.models.progress import UserQuestionAttempt
from app.schemas.question import AnswerSubmit, AnswerResult, LearningSession, WrongQuestionItem, ReportSubmit
from app.services.learning_engine import LearningEngine
from app.core.pagination import PaginationParams, PaginatedResponse, paginate_query

router = APIRouter(prefix="/learn", tags=["Learning"])


@router.get("/next-question/{subject_id}", response_model=LearningSession)
def get_next_question(
    subject_id: str,
    concept_id: str | None = Query(None, description="Focus on a specific concept"),
    topic_id: str | None = Query(None, description="Focus on a specific topic"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get the next adaptive question. Optionally scoped to a concept or topic."""
    engine = LearningEngine(db, user.id)
    session = engine.get_next_question(subject_id, concept_id=concept_id, topic_id=topic_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="No more questions available. You've covered everything!",
        )
    return session


@router.post("/submit-answer", response_model=AnswerResult)
def submit_answer(
    answer: AnswerSubmit,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Submit an answer and receive feedback + updated progress."""
    engine = LearningEngine(db, user.id)
    try:
        result = engine.submit_answer(answer)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result


@router.get("/wrong-questions/{subject_id}", response_model=PaginatedResponse[WrongQuestionItem])
def get_wrong_questions(
    subject_id: str,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get questions the user answered incorrectly, with attempt counts."""
    # Subquery: concept IDs in this subject
    subject_concept_ids = (
        db.query(Concept.id)
        .join(Topic, Concept.topic_id == Topic.id)
        .filter(Topic.subject_id == subject_id)
        .subquery()
    )

    # Subquery: questions the user has since answered correctly (exclude from wrong list)
    correctly_answered = (
        db.query(UserQuestionAttempt.question_id)
        .filter(
            UserQuestionAttempt.user_id == user.id,
            UserQuestionAttempt.is_correct == True,
            UserQuestionAttempt.concept_id.in_(subject_concept_ids.select()),
        )
        .distinct()
        .subquery()
    )

    # Get distinct wrong question IDs with latest attempt info
    wrong_attempts = (
        db.query(
            UserQuestionAttempt.question_id,
            func.count(UserQuestionAttempt.id).label("attempt_count"),
            func.max(UserQuestionAttempt.attempted_at).label("last_attempted"),
            func.max(UserQuestionAttempt.selected_answer).label("last_answer"),
        )
        .filter(
            UserQuestionAttempt.user_id == user.id,
            UserQuestionAttempt.is_correct == False,
            UserQuestionAttempt.concept_id.in_(subject_concept_ids.select()),
            UserQuestionAttempt.question_id.notin_(correctly_answered.select()),
        )
        .group_by(UserQuestionAttempt.question_id)
        .order_by(func.max(UserQuestionAttempt.attempted_at).desc())
    )

    # Get total count
    total = wrong_attempts.count()
    rows = wrong_attempts.offset(pagination.offset).limit(pagination.page_size).all()

    items = []
    # Batch-fetch question + concept + topic data in one query
    qids = [row[0] for row in rows]
    if qids:
        q_data = (
            db.query(Question, Concept.id, Concept.name, Topic.name)
            .join(QuestionConcept, QuestionConcept.question_id == Question.id)
            .join(Concept, Concept.id == QuestionConcept.concept_id)
            .join(Topic, Topic.id == Concept.topic_id)
            .filter(Question.id.in_(qids))
            .all()
        )
        q_map = {q.id: (q, cid, cn, tn) for q, cid, cn, tn in q_data}
    else:
        q_map = {}

    for qid, attempt_count, last_attempted, last_answer in rows:
        entry = q_map.get(qid)
        if not entry:
            continue
        q, concept_id, concept_name, topic_name = entry

        items.append(WrongQuestionItem(
            question_id=qid,
            question_text=q.question_text,
            correct_answer=q.correct_answer,
            selected_answer=last_answer or "",
            explanation=q.explanation,
            concept_id=concept_id,
            concept_name=concept_name,
            topic_name=topic_name,
            difficulty=q.difficulty,
            attempt_count=attempt_count,
            last_attempted=str(last_attempted) if last_attempted else "",
        ))

    return PaginatedResponse.create(items, total, pagination)


@router.get("/concept-notes/{concept_id}")
def get_concept_notes(
    concept_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get detailed notes for a concept — explanation + key points."""
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    topic = db.query(Topic).filter(Topic.id == concept.topic_id).first()

    return {
        "id": concept.id,
        "name": concept.name,
        "topic_name": topic.name if topic else "",
        "explanation": concept.explanation,
        "key_points": json.loads(concept.key_points) if isinstance(concept.key_points, str) else (concept.key_points or []),
    }


@router.post("/report-question")
def report_question(
    report: ReportSubmit,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Report a question as incorrect, unclear, or problematic."""
    import uuid

    question = db.query(Question).filter(Question.id == report.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Check for duplicate report from same user
    existing = (
        db.query(QuestionReport)
        .filter(
            QuestionReport.question_id == report.question_id,
            QuestionReport.user_id == user.id,
            QuestionReport.status == "pending",
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="You've already reported this question")

    new_report = QuestionReport(
        id=str(uuid.uuid4()),
        question_id=report.question_id,
        user_id=user.id,
        reason=report.reason,
        details=report.details,
    )
    db.add(new_report)

    # Get total report count for this question
    report_count = (
        db.query(func.count(QuestionReport.id))
        .filter(QuestionReport.question_id == report.question_id)
        .scalar()
    ) or 0

    db.commit()

    return {
        "message": "Report submitted. Thank you for helping improve MasterCS!",
        "report_count": report_count + 1,
    }


@router.get("/question-reports/{question_id}")
def get_question_reports(
    question_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get report count for a question and whether current user has reported it."""
    total = (
        db.query(func.count(QuestionReport.id))
        .filter(QuestionReport.question_id == question_id)
        .scalar()
    ) or 0

    user_reported = (
        db.query(QuestionReport)
        .filter(
            QuestionReport.question_id == question_id,
            QuestionReport.user_id == user.id,
        )
        .first()
    ) is not None

    return {"report_count": total, "user_reported": user_reported}
