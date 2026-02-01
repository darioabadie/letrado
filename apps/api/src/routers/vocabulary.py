from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models import User, UserWord, Word
from ..schemas import UserWordOut, UserWordUpdate, WordCreated, WordsCreate, WordsCreatedResponse


router = APIRouter(prefix="/users/{user_id}/words", tags=["vocabulary"])


@router.post("", response_model=WordsCreatedResponse, status_code=status.HTTP_201_CREATED)
def add_words(user_id: UUID, payload: WordsCreate, db: Session = Depends(get_db)) -> WordsCreatedResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    created: list[WordCreated] = []
    for raw_word in payload.words:
        word_text = raw_word.strip().lower()
        if not word_text:
            continue

        word = db.query(Word).filter(Word.text == word_text).first()
        if not word:
            word = Word(text=word_text)
            db.add(word)
            db.flush()

        existing = (
            db.query(UserWord)
            .filter(UserWord.user_id == user_id, UserWord.word_id == word.id)
            .first()
        )
        if existing:
            continue

        user_word = UserWord(user_id=user_id, word_id=word.id, status="latent")
        db.add(user_word)
        created.append(WordCreated(word_id=word.id, text=word.text, status="latent"))

    db.commit()
    return WordsCreatedResponse(created=created)


@router.get("", response_model=list[UserWordOut])
def list_words(user_id: UUID, db: Session = Depends(get_db)) -> list[UserWordOut]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    rows = (
        db.query(UserWord, Word)
        .join(Word, Word.id == UserWord.word_id)
        .filter(UserWord.user_id == user_id)
        .all()
    )

    return [
        UserWordOut(
            word_id=word.id,
            text=word.text,
            status=user_word.status,
            correct_uses=user_word.correct_uses,
            last_used_at=user_word.last_used_at,
        )
        for user_word, word in rows
    ]


@router.patch("/{word_id}", response_model=UserWordOut)
def update_user_word(
    user_id: UUID,
    word_id: int,
    payload: UserWordUpdate,
    db: Session = Depends(get_db),
) -> UserWordOut:
    user_word = (
        db.query(UserWord)
        .filter(UserWord.user_id == user_id, UserWord.word_id == word_id)
        .first()
    )
    if not user_word:
        raise HTTPException(status_code=404, detail="user word not found")

    if payload.status is not None:
        user_word.status = payload.status.value
    if payload.correct_uses is not None:
        user_word.correct_uses = payload.correct_uses

    db.commit()
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="word not found")

    return UserWordOut(
        word_id=word.id,
        text=word.text,
        status=user_word.status,
        correct_uses=user_word.correct_uses,
        last_used_at=user_word.last_used_at,
    )
