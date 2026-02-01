from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models import Prompt, User
from ..schemas import PromptCreate, PromptOut


router = APIRouter(prefix="/users/{user_id}/prompts", tags=["prompts"])


@router.post("", response_model=PromptOut, status_code=status.HTTP_201_CREATED)
def create_prompt(user_id: UUID, payload: PromptCreate, db: Session = Depends(get_db)) -> PromptOut:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    prompt = Prompt(user_id=user_id, content=payload.content, scheduled_for=payload.scheduled_for)
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    return prompt


@router.get("", response_model=list[PromptOut])
def list_prompts(user_id: UUID, db: Session = Depends(get_db)) -> list[PromptOut]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    prompts = (
        db.query(Prompt)
        .filter(Prompt.user_id == user_id)
        .order_by(Prompt.scheduled_for.desc())
        .all()
    )
    return prompts
