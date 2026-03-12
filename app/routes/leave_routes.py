from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.controllers.leave_controller import (
    get_leave_requests,
    approve_leave,
    reject_leave
)

router = APIRouter(prefix="/admin", tags=["Leave Management"])


@router.get("/leave-requests")
def get_leave_requests_route(db: Session = Depends(get_db)):
    return get_leave_requests(db)


@router.patch("/leave-requests/{leave_id}/approve")
def approve_leave_route(
    leave_id: int,
    db: Session = Depends(get_db)
):
    return approve_leave(leave_id, db)


@router.patch("/leave-requests/{leave_id}/reject")
def reject_leave_route(
    leave_id: int,
    rejection_reason: str,
    db: Session = Depends(get_db)
):
    return reject_leave(leave_id, rejection_reason, db)