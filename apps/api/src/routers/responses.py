from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models import Prompt, Response, User
from ..schemas import ResponseCreate, ResponseOut


router = APIRouter(prefix="/users/{user_id}/responses", tags=["responses"])


@router.post("", response_model=ResponseOut, status_code=status.HTTP_201_CREATED)
def create_response(user_id: UUID, payload: ResponseCreate, db: Session = Depends(get_db)) -> ResponseOut:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    prompt = (
        db.query(Prompt)
        .filter(Prompt.id == payload.prompt_id, Prompt.user_id == user_id)
        .first()
    )
    if not prompt:
        raise HTTPException(status_code=404, detail="prompt not found")

    response = Response(
        user_id=user_id,
        prompt_id=payload.prompt_id,
        content=payload.content,
        is_valid=False,
    )
    db.add(response)
    db.commit()
    db.refresh(response)
    return response


@router.get("", response_model=list[ResponseOut])
def list_responses(user_id: UUID, db: Session = Depends(get_db)) -> list[ResponseOut]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    responses = (
        db.query(Response)
        .filter(Response.user_id == user_id)
        .order_by(Response.created_at.desc())
        .all()
    )
    return responses
