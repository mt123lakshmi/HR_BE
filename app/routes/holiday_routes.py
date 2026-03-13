from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.holiday_schema import HolidayCreate,HolidayUpdate
from app.controllers.holiday_controller import (
    create_holiday,
    get_all_holidays,
    get_holiday_by_id,
    update_holiday,
    delete_holiday
)

from app.database.database import get_db

router = APIRouter(
    prefix="/admin",
    tags=["Holiday Management"]
)


@router.post("/holiday")
def add_holiday(
    holiday: HolidayCreate,
    db: Session = Depends(get_db)
):
    return create_holiday(db, holiday, user_id=1)


@router.get("/holiday")
def list_holidays(
    db: Session = Depends(get_db)
):
    return get_all_holidays(db)


@router.get("/{holiday_id}")
def get_holiday(
    holiday_id: int,
    db: Session = Depends(get_db)
):
    return get_holiday_by_id(db, holiday_id)


@router.put("/{holiday_id}")
def update_holiday_api(
    holiday_id: int,
    holiday: HolidayUpdate,
    db: Session = Depends(get_db)
):
    return update_holiday(db, holiday_id, holiday)


@router.delete("/{holiday_id}")
def delete_holiday_api(
    holiday_id: int,
    db: Session = Depends(get_db)
):
    return delete_holiday(db, holiday_id)