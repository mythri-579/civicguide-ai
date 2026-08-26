from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.update_alert import UpdateAlert
from app.schemas.update_alert import UpdateAlertResponse
from app.services.update_monitor_service import check_all_sources
from app.services.approval_service import approve_update, reject_update

router = APIRouter(prefix="/api/sources", tags=["Source Monitor"])


@router.post("/check-updates")
def trigger_check(db: Session = Depends(get_db)):
    result = check_all_sources(db)
    return result


@router.get("/alerts", response_model=list[UpdateAlertResponse])
def list_alerts(db: Session = Depends(get_db)):
    return (
        db.query(UpdateAlert)
        .filter(UpdateAlert.status == "pending")
        .order_by(UpdateAlert.detected_at.desc())
        .all()
    )


@router.post("/approve-update/{alert_id}")
def approve(alert_id: int, db: Session = Depends(get_db)):
    try:
        result = approve_update(db, alert_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reject-update/{alert_id}")
def reject(alert_id: int, db: Session = Depends(get_db)):
    try:
        result = reject_update(db, alert_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))