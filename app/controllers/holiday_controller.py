from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.models import Holiday


def create_holiday(db: Session, holiday, user_id):

    existing = db.query(Holiday).filter(
        Holiday.holiday_date == holiday.holiday_date
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Holiday already exists for this date"
        )

    new_holiday = Holiday(
        title=holiday.title,
        type=holiday.type,
        holiday_date=holiday.holiday_date,
        description=holiday.description,
        created_by=user_id
    )

    db.add(new_holiday)
    db.commit()
    db.refresh(new_holiday)

    return new_holiday


def get_all_holidays(db: Session):

    holidays = db.query(Holiday).order_by(Holiday.holiday_date).all()

    return holidays


def get_holiday_by_id(db: Session, holiday_id: int):

    holiday = db.query(Holiday).filter(Holiday.id == holiday_id).first()

    if not holiday:
        raise HTTPException(status_code=404, detail="Holiday not found")

    return holiday


def update_holiday(db: Session, holiday_id: int, holiday_data):

    holiday = db.query(Holiday).filter(Holiday.id == holiday_id).first()

    if not holiday:
        raise HTTPException(status_code=404, detail="Holiday not found")

    holiday.title = holiday_data.title
    holiday.type = holiday_data.type
    holiday.holiday_date = holiday_data.holiday_date
    holiday.description = holiday_data.description

    db.commit()
    db.refresh(holiday)

    return holiday


def delete_holiday(db: Session, holiday_id: int):

    holiday = db.query(Holiday).filter(Holiday.id == holiday_id).first()

    if not holiday:
        raise HTTPException(status_code=404, detail="Holiday not found")

    db.delete(holiday)
    db.commit()

    return {"message": "Holiday deleted successfully"}