from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models import TTRMetric, User
from ..schemas import TTRMetricOut


router = APIRouter(prefix="/users/{user_id}/metrics", tags=["metrics"])


@router.get("/ttr", response_model=TTRMetricOut)
def get_ttr(user_id: UUID, db: Session = Depends(get_db)) -> TTRMetricOut:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    metric = (
        db.query(TTRMetric)
        .filter(TTRMetric.user_id == user_id)
        .order_by(TTRMetric.calculated_at.desc())
        .first()
    )
    if not metric:
        raise HTTPException(status_code=404, detail="ttr metric not found")

    return TTRMetricOut(ttr=metric.ttr, calculated_at=metric.calculated_at)
