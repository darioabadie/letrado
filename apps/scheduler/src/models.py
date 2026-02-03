import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    whatsapp_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String(120))
    goal: Mapped[str] = mapped_column(String(40), nullable=False)
    timezone: Mapped[str] = mapped_column(String(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)


class UserWord(Base):
    __tablename__ = "user_words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    word_id: Mapped[int] = mapped_column(Integer, ForeignKey("words.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="latent")
    correct_uses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime)


class Prompt(Base):
    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    scheduled_for: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime)
