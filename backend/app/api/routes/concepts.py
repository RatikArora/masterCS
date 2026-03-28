"""Concept and topic browsing routes — optimized with JOINs, no N+1 queries."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.core.pagination import PaginationParams, PaginatedResponse, paginate_query
from app.models.user import User
from app.models.subject import Subject, Topic
from app.models.concept import Concept
from app.models.question import QuestionConcept
from app.models.progress import UserConceptProgress
from app.schemas.concept import SubjectResponse, TopicResponse, ConceptResponse, ConceptDetailResponse

router = APIRouter(prefix="/concepts", tags=["Concepts"])


@router.get("/subjects", response_model=list[SubjectResponse])
def list_subjects(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """List subjects filtered by user's degree — single query with aggregation."""
    # Filter subjects by user's degree if they have one set
    base_query = db.query(Subject)
    if user.degree:
        # Filter to subjects whose target_degrees contains the user's degree
        base_query = base_query.filter(
            Subject.target_degrees.like(f"%{user.degree}%")
        )

    subject_ids = [s.id for s in base_query.all()]

    # Subquery: count topics per subject
    topic_counts = (
        db.query(Topic.subject_id, func.count(Topic.id).label("cnt"))
        .group_by(Topic.subject_id)
        .subquery()
    )

    # Subquery: weighted progress per subject (all started concepts contribute)
    # novice=0, learning=0.2, familiar=0.5, proficient=0.8, mastered=1.0
    progress_scores = (
        db.query(
            Topic.subject_id,
            func.sum(case(
                (UserConceptProgress.mastery_level == "mastered", 1.0),
                (UserConceptProgress.mastery_level == "proficient", 0.8),
                (UserConceptProgress.mastery_level == "familiar", 0.5),
                (UserConceptProgress.mastery_level == "learning", 0.2),
                else_=0.0,
            )).label("weighted_score"),
        )
        .join(Concept, Concept.topic_id == Topic.id)
        .join(
            UserConceptProgress,
            (UserConceptProgress.concept_id == Concept.id) & (UserConceptProgress.user_id == user.id),
        )
        .group_by(Topic.subject_id)
        .subquery()
    )

    # Subquery: total concepts per subject
    concept_counts = (
        db.query(Topic.subject_id, func.count(Concept.id).label("total"))
        .join(Concept, Concept.topic_id == Topic.id)
        .group_by(Topic.subject_id)
        .subquery()
    )

    rows = (
        db.query(
            Subject,
            func.coalesce(topic_counts.c.cnt, 0).label("topic_count"),
            func.coalesce(progress_scores.c.weighted_score, 0).label("weighted"),
            func.coalesce(concept_counts.c.total, 0).label("total_concepts"),
        )
        .filter(Subject.id.in_(subject_ids))
        .outerjoin(topic_counts, Subject.id == topic_counts.c.subject_id)
        .outerjoin(progress_scores, Subject.id == progress_scores.c.subject_id)
        .outerjoin(concept_counts, Subject.id == concept_counts.c.subject_id)
        .order_by(Subject.order_index)
        .all()
    )

    return [
        SubjectResponse(
            id=s.id, name=s.name, description=s.description,
            icon=s.icon, color=s.color, order_index=s.order_index,
            topic_count=tc,
            progress_percent=round((float(w) / t) * 100, 1) if t > 0 else 0.0,
        )
        for s, tc, w, t in rows
    ]


@router.get("/subjects/{subject_id}/topics", response_model=PaginatedResponse[TopicResponse])
def list_topics(
    subject_id: str,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """List topics with concept count and mastery — paginated, no N+1."""
    base_query = (
        db.query(Topic)
        .filter(Topic.subject_id == subject_id)
        .order_by(Topic.order_index)
    )
    topics, total = paginate_query(base_query, pagination)

    if not topics:
        return PaginatedResponse.create([], total, pagination)

    topic_ids = [t.id for t in topics]

    # Single aggregation query: concept count + mastery stats per topic
    stats = (
        db.query(
            Concept.topic_id,
            func.count(Concept.id).label("concept_count"),
            func.count(UserConceptProgress.id).label("started"),
            func.sum(case(
                (UserConceptProgress.mastery_level.in_(["proficient", "mastered"]), 1),
                else_=0,
            )).label("mastered_count"),
            func.coalesce(func.avg(UserConceptProgress.confidence_score), 0).label("avg_conf"),
        )
        .outerjoin(
            UserConceptProgress,
            (UserConceptProgress.concept_id == Concept.id) & (UserConceptProgress.user_id == user.id),
        )
        .filter(Concept.topic_id.in_(topic_ids))
        .group_by(Concept.topic_id)
        .all()
    )

    stats_map = {s[0]: s for s in stats}

    # Question count per topic
    q_counts = (
        db.query(
            Concept.topic_id,
            func.count(QuestionConcept.question_id).label("q_count"),
        )
        .join(QuestionConcept, QuestionConcept.concept_id == Concept.id)
        .filter(Concept.topic_id.in_(topic_ids))
        .group_by(Concept.topic_id)
        .all()
    )
    q_map = {tid: cnt for tid, cnt in q_counts}

    items = [
        TopicResponse(
            id=t.id, subject_id=t.subject_id, name=t.name,
            description=t.description, icon=t.icon, order_index=t.order_index,
            concept_count=int(stats_map[t.id][1]) if t.id in stats_map else 0,
            question_count=q_map.get(t.id, 0),
            mastery_percent=round(
                (int(stats_map[t.id][3] or 0) / int(stats_map[t.id][1])) * 100, 1
            ) if t.id in stats_map and int(stats_map[t.id][1]) > 0 else 0.0,
            is_unlocked=True,
        )
        for t in topics
    ]

    return PaginatedResponse.create(items, total, pagination)


@router.get("/topics/{topic_id}/concepts", response_model=PaginatedResponse[ConceptResponse])
def list_concepts(
    topic_id: str,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """List concepts with user progress — paginated, single LEFT JOIN query."""
    base_query = (
        db.query(Concept, UserConceptProgress)
        .outerjoin(
            UserConceptProgress,
            (UserConceptProgress.concept_id == Concept.id) & (UserConceptProgress.user_id == user.id),
        )
        .filter(Concept.topic_id == topic_id)
        .order_by(Concept.order_index)
    )

    total = base_query.count()
    rows = base_query.offset(pagination.offset).limit(pagination.page_size).all()

    items = [
        ConceptResponse(
            id=c.id, topic_id=c.topic_id, name=c.name,
            explanation=c.explanation, key_points=c.key_points,
            order_index=c.order_index,
            mastery_level=p.mastery_level if p else "novice",
            confidence_score=p.confidence_score if p else 0.0,
        )
        for c, p in rows
    ]

    return PaginatedResponse.create(items, total, pagination)


@router.get("/concept/{concept_id}", response_model=ConceptDetailResponse)
def get_concept_detail(
    concept_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get concept detail — single joined query."""
    row = (
        db.query(Concept, Topic, Subject, UserConceptProgress)
        .join(Topic, Concept.topic_id == Topic.id)
        .join(Subject, Topic.subject_id == Subject.id)
        .outerjoin(
            UserConceptProgress,
            (UserConceptProgress.concept_id == Concept.id) & (UserConceptProgress.user_id == user.id),
        )
        .filter(Concept.id == concept_id)
        .first()
    )

    if not row:
        raise HTTPException(status_code=404, detail="Concept not found")

    concept, topic, subject, progress = row
    question_count = db.query(func.count(QuestionConcept.question_id)).filter(
        QuestionConcept.concept_id == concept_id
    ).scalar()

    total = (progress.correct_count + progress.incorrect_count) if progress else 0
    accuracy = (progress.correct_count / total * 100) if total > 0 else 0.0

    return ConceptDetailResponse(
        id=concept.id, topic_id=concept.topic_id, name=concept.name,
        explanation=concept.explanation, key_points=concept.key_points,
        order_index=concept.order_index,
        mastery_level=progress.mastery_level if progress else "novice",
        confidence_score=progress.confidence_score if progress else 0.0,
        topic_name=topic.name, subject_name=subject.name,
        question_count=question_count, attempts_count=total,
        accuracy=round(accuracy, 1),
    )
