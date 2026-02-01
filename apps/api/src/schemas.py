from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class GoalEnum(str, Enum):
    professional = "professional"
    academic = "academic"
    creative = "creative"


class WordStatusEnum(str, Enum):
    latent = "latent"
    practice = "practice"
    active = "active"


class UserCreate(BaseModel):
    whatsapp_id: str = Field(..., min_length=1, max_length=64)
    name: str | None = Field(default=None, max_length=120)
    goal: GoalEnum
    timezone: str = Field(..., min_length=1, max_length=80)


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=120)
    goal: GoalEnum | None = None
    timezone: str | None = Field(default=None, max_length=80)


class UserOut(BaseModel):
    id: UUID
    whatsapp_id: str
    name: str | None
    goal: GoalEnum
    timezone: str
    created_at: datetime

    class Config:
        from_attributes = True


class WordsCreate(BaseModel):
    words: list[str] = Field(..., min_length=1)


class UserWordOut(BaseModel):
    word_id: int
    text: str
    status: WordStatusEnum
    correct_uses: int
    last_used_at: datetime | None


class UserWordUpdate(BaseModel):
    status: WordStatusEnum | None = None
    correct_uses: int | None = None


class WordCreated(BaseModel):
    word_id: int
    text: str
    status: WordStatusEnum


class WordsCreatedResponse(BaseModel):
    created: list[WordCreated]


class PromptCreate(BaseModel):
    content: str = Field(..., min_length=1)
    scheduled_for: datetime


class PromptOut(BaseModel):
    id: int
    content: str
    scheduled_for: datetime
    sent_at: datetime | None

    class Config:
        from_attributes = True


class ResponseCreate(BaseModel):
    prompt_id: int
    content: str = Field(..., min_length=1)


class ResponseOut(BaseModel):
    id: int
    prompt_id: int
    is_valid: bool
    feedback: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class TTRMetricOut(BaseModel):
    ttr: float
    calculated_at: datetime


class WhatsAppWebhookIn(BaseModel):
    from_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
    timestamp: datetime


class WebhookAccepted(BaseModel):
    status: str = "accepted"
