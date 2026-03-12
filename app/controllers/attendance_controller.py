from sqlalchemy.orm import Session
from datetime import date, timedelta
from calendar import monthrange

from app.models.models import LeaveRequest, Holiday, Employee


def get_attendance_overview(year: int, month: int, db: Session):

    start_date = date(year, month, 1)
    last_day = monthrange(year, month)[1]
    end_date = date(year, month, last_day)

    calendar_data = []

    current_day = start_date

    while current_day <= end_date:

        status = "Working Day"
        description = None

        # 1️⃣ Holiday check
        holiday = db.query(Holiday).filter(
            Holiday.holiday_date == current_day
        ).first()

        if holiday:
            status = "Holiday"
            description = holiday.title

        # 2️⃣ Leave check
        leave = db.query(LeaveRequest).filter(
            LeaveRequest.start_date <= current_day,
            LeaveRequest.end_date >= current_day,
            LeaveRequest.status == "Approved"
        ).first()

        if leave:
            employee = db.query(Employee).filter(
                Employee.id == leave.employee_id
            ).first()

            status = "Employee Leave"
            description = f"{leave.leave_type}: {leave.reason}"
            employee_name = employee.name if employee else None
        else:
            employee_name = None

        # 3️⃣ Weekend check
        if current_day.weekday() >= 5 and status == "Working Day":
            status = "Weekend"

        calendar_data.append({
            "date": current_day,
            "status": status,
            "employee": employee_name,
            "description": description
        })

        current_day += timedelta(days=1)

    return calendar_data

def get_attendance_day_details(selected_date: date, db: Session):

    # Holiday check
    holiday = db.query(Holiday).filter(
        Holiday.holiday_date == selected_date
    ).first()

    if holiday:
        return {
            "type": "Holiday",
            "title": holiday.title,
            "description": holiday.description
        }

    # Leave check
    leave = db.query(LeaveRequest).filter(
        LeaveRequest.start_date <= selected_date,
        LeaveRequest.end_date >= selected_date,
        LeaveRequest.status == "Approved"
    ).first()

    if leave:

        employee = db.query(Employee).filter(
            Employee.id == leave.employee_id
        ).first()

        return {
            "type": "Employee Leave",
            "employee": employee.name if employee else None,
            "leave_type": leave.leave_type,
            "reason": leave.reason
        }

    # Weekend check
    if selected_date.weekday() >= 5:
        return {
            "type": "Weekend"
        }

    return {
        "type": "Working Day"
    }