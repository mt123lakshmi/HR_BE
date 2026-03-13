from datetime import date, timedelta
from calendar import monthrange
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.models import LeaveRequest, Holiday, Employee


def get_attendance_overview(year: int, month: int, db: Session):

    start_date = date(year, month, 1)
    last_day = monthrange(year, month)[1]
    end_date = date(year, month, last_day)

    # 1️⃣ Fetch holidays for the month (1 query)
    holidays = db.query(Holiday).filter(
        Holiday.holiday_date.between(start_date, end_date)
    ).all()

    holiday_map = {h.holiday_date: h for h in holidays}

    # 2️⃣ Fetch approved leaves overlapping the month (1 query)
    leaves = db.query(LeaveRequest, Employee).join(
        Employee, Employee.id == LeaveRequest.employee_id
    ).filter(
        LeaveRequest.status == "Approved",
        LeaveRequest.start_date <= end_date,
        LeaveRequest.end_date >= start_date
    ).all()

    leave_map = {}

    for leave, employee in leaves:

        current = leave.start_date

        while current <= leave.end_date:

            if start_date <= current <= end_date:

                if current not in leave_map:
                    leave_map[current] = []

                leave_map[current].append({
                    "employee": employee.name,
                    "leave_type": leave.leave_type,
                    "reason": leave.reason
                })

            current += timedelta(days=1)

    # 3️⃣ Build calendar
    calendar = []
    current_day = start_date

    while current_day <= end_date:

        status = "Working Day"
        description = None

        if current_day in holiday_map:
            status = "Holiday"
            description = holiday_map[current_day].title

        elif current_day in leave_map:
            status = "Employee Leave"
            description = leave_map[current_day]

        elif current_day.weekday() >= 5:
            status = "Weekend"

        calendar.append({
            "date": current_day,
            "status": status,
            "details": description
        })

        current_day += timedelta(days=1)

    return calendar

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