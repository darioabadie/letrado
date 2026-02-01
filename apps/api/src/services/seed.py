from sqlalchemy.orm import Session

from ..models import UserWord, Word
from ..preset_words import get_preset_words


def seed_user_words(db: Session, user_id, goal: str) -> None:
    for raw_word in get_preset_words(goal):
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

        db.add(UserWord(user_id=user_id, word_id=word.id, status="latent"))
