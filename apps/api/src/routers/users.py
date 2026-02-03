from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models import User
from ..schemas import UserCreate, UserOut, UserUpdate
from ..services.seed import seed_user_words


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    existing = db.query(User).filter(User.whatsapp_id == payload.whatsapp_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="whatsapp_id already exists")

    user = User(
        whatsapp_id=payload.whatsapp_id,
        name=payload.name,
        goal=payload.goal.value,
        timezone=payload.timezone,
        onboarding_step="completed",
    )
    db.add(user)
    db.flush()
    seed_user_words(db, user.id, user.goal)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: UUID, db: Session = Depends(get_db)) -> UserOut:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: UUID, payload: UserUpdate, db: Session = Depends(get_db)) -> UserOut:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    if payload.name is not None:
        user.name = payload.name
    if payload.goal is not None:
        user.goal = payload.goal.value
    if payload.timezone is not None:
        user.timezone = payload.timezone

    db.commit()
    db.refresh(user)
    return user
