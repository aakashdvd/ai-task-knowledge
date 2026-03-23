from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_admin
from app.models import User
from app.schemas.analytics import AnalyticsResponse
from app.services.analytics_service import get_basic_analytics

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("", response_model=AnalyticsResponse)
def read_analytics(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    return get_basic_analytics(db=db) 