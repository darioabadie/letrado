import os
from datetime import datetime, time, timezone
from zoneinfo import ZoneInfo

from celery import Celery
from celery.schedules import crontab
from sqlalchemy import case, func

from .db import SessionLocal
from .models import Prompt, User, UserWord, Word


broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")

celery_app = Celery("letrado_scheduler", broker=broker_url, backend=result_backend)
celery_app.conf.timezone = "UTC"
celery_app.conf.beat_schedule = {
    "daily-prompts": {
        "task": "src.scheduler.generate_daily_prompts",
        "schedule": crontab(minute=0),
    }
}


def _safe_timezone(timezone_name: str | None) -> ZoneInfo:
    if not timezone_name:
        return ZoneInfo("UTC")
    try:
        return ZoneInfo(timezone_name)
    except Exception:
        return ZoneInfo("UTC")


def _should_send_prompt(local_now: datetime, preferred_hour: int | None) -> bool:
    hour = preferred_hour if preferred_hour is not None else 9
    return local_now.hour == hour


def _words_per_prompt(days_since_created: int) -> tuple[int, int]:
    if days_since_created <= 2:
        return 1, 2
    return 2, 3


def _build_prompt_text(words: list[str]) -> str:
    return "Escribe una frase usando: " + ", ".join(words)


@celery_app.task(name="src.scheduler.generate_daily_prompts")
def generate_daily_prompts() -> dict[str, int]:
    now_utc = datetime.now(timezone.utc)
    created = 0
    with SessionLocal() as db:
        users = db.query(User).all()
        for user in users:
            tz = _safe_timezone(user.timezone)
            local_now = now_utc.astimezone(tz)
            if not _should_send_prompt(local_now, user.preferred_hour):
                continue

            local_date = local_now.date()
            local_target = datetime.combine(local_date, time(hour=9, minute=0, tzinfo=tz))
            scheduled_for = local_target.astimezone(timezone.utc).replace(tzinfo=None)
            target_date = scheduled_for.date()

            existing = (
                db.query(Prompt)
                .filter(Prompt.user_id == user.id)
                .filter(func.date(Prompt.scheduled_for) == target_date)
                .first()
            )
            if existing:
                continue

            created_at = user.created_at.replace(tzinfo=timezone.utc).astimezone(tz)
            days_since_created = (local_date - created_at.date()).days
            min_words, max_words = _words_per_prompt(days_since_created)

            ordering = (
                case((UserWord.status == "latent", 0), (UserWord.status == "practice", 1), else_=2),
                UserWord.last_used_at.is_(None).desc(),
                UserWord.last_used_at.asc(),
                UserWord.id.asc(),
            )
            rows = (
                db.query(UserWord, Word)
                .join(Word, Word.id == UserWord.word_id)
                .filter(UserWord.user_id == user.id)
                .filter(UserWord.status.in_(["latent", "practice"]))
                .order_by(*ordering)
                .limit(max_words)
                .all()
            )
            if not rows:
                continue

            selected_count = min(max_words, len(rows))
            if selected_count < min_words and len(rows) < min_words:
                selected_count = len(rows)
            selected = rows[:selected_count]
            words = [word.text for _, word in selected]
            if not words:
                continue

            prompt = Prompt(
                user_id=user.id,
                content=_build_prompt_text(words),
                scheduled_for=scheduled_for,
            )
            db.add(prompt)
            for user_word, _ in selected:
                if user_word.status == "latent":
                    user_word.status = "practice"
            created += 1

        db.commit()

    return {"created": created}
