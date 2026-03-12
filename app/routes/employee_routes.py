from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.controllers.employee_controller import get_employee_dashboard,get_employee_profile

router = APIRouter(prefix="/employee", tags=["Employee"])


@router.get("/dashboard")
def employee_dashboard(
    employee_id: int,
    db: Session = Depends(get_db)
):
    return get_employee_dashboard(employee_id, db)


@router.get("/profile/{employee_id}")
def employee_profile(employee_id: int, db: Session = Depends(get_db)):
    return get_employee_profile(employee_id, db)