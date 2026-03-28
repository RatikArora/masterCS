"""Authentication routes — register, login, profile management."""

import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.progress import UserConceptProgress, UserQuestionAttempt, UserDailyStats
from app.models.concept import Concept
from app.models.subject import Topic
from app.schemas.user import UserCreate, UserLogin, UserUpdate, UserResponse, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    # Check duplicates
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        id=str(uuid.uuid4()),
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        display_name=data.display_name or data.username,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.id})
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.id})
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
def get_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return UserResponse.model_validate(current_user)


@router.patch("/profile", response_model=UserResponse)
def update_profile(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update user profile — display name, degree, course."""
    if data.display_name is not None:
        current_user.display_name = data.display_name
    if data.degree is not None:
        current_user.degree = data.degree
    if data.course is not None:
        current_user.course = data.course
    db.commit()
    db.refresh(current_user)
    return UserResponse.model_validate(current_user)


@router.post("/reset-progress/{subject_id}")
def reset_subject_progress(
    subject_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Reset all progress for a subject. Deletes attempts, concept progress, and daily stats XP."""
    concept_ids = (
        db.query(Concept.id)
        .join(Topic, Concept.topic_id == Topic.id)
        .filter(Topic.subject_id == subject_id)
        .all()
    )
    cids = [c[0] for c in concept_ids]
    if not cids:
        raise HTTPException(status_code=404, detail="Subject not found or has no concepts")

    # Delete attempts for these concepts
    deleted_attempts = (
        db.query(UserQuestionAttempt)
        .filter(UserQuestionAttempt.user_id == current_user.id, UserQuestionAttempt.concept_id.in_(cids))
        .delete(synchronize_session=False)
    )
    # Delete concept progress
    deleted_progress = (
        db.query(UserConceptProgress)
        .filter(UserConceptProgress.user_id == current_user.id, UserConceptProgress.concept_id.in_(cids))
        .delete(synchronize_session=False)
    )
    db.commit()
    return {"message": "Progress reset successfully", "attempts_deleted": deleted_attempts, "concepts_reset": deleted_progress}


@router.post("/reset-topic/{topic_id}")
def reset_topic_progress(
    topic_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Reset progress for a single topic."""
    concept_ids = (
        db.query(Concept.id)
        .filter(Concept.topic_id == topic_id)
        .all()
    )
    cids = [c[0] for c in concept_ids]
    if not cids:
        raise HTTPException(status_code=404, detail="Topic not found")

    db.query(UserQuestionAttempt).filter(
        UserQuestionAttempt.user_id == current_user.id, UserQuestionAttempt.concept_id.in_(cids)
    ).delete(synchronize_session=False)
    db.query(UserConceptProgress).filter(
        UserConceptProgress.user_id == current_user.id, UserConceptProgress.concept_id.in_(cids)
    ).delete(synchronize_session=False)
    db.commit()
    return {"message": "Topic progress reset successfully"}
