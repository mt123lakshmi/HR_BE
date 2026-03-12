from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.database.database import get_db
from app.controllers.attendance_controller import (
    get_attendance_overview,
    get_attendance_day_details
)

router = APIRouter(prefix="/admin", tags=["Attendance"])


@router.get("/attendance-overview")
def attendance_overview(year: int, month: int, db: Session = Depends(get_db)):
    return get_attendance_overview(year, month, db)


@router.get("/attendance-overview/{selected_date}")
def attendance_day_details(selected_date: date, db: Session = Depends(get_db)):
    return get_attendance_day_details(selected_date, db)