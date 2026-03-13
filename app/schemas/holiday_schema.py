from pydantic import BaseModel
from datetime import date


class HolidayCreate(BaseModel):
    title: str
    type: str
    holiday_date: date
    description: str


class HolidayUpdate(BaseModel):
    title: str
    type: str
    holiday_date: date
    description: str


class HolidayResponse(BaseModel):
    id: int
    title: str
    type: str
    holiday_date: date
    description: str

    class Config:
        from_attributes = True