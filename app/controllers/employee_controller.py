from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.models.models import (
    Employee,
    LeaveRequest,
    LeaveBalance,
    Holiday,
    Designation,
    Department,
    EmployeeFinancialDetail,
    EmployeeAsset,
    Payroll
)


def get_employee_dashboard(employee_id: int, db: Session):

    today = date.today()

    # Employee info
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        return {
            "error": "Employee not found"
        }


    designation = db.query(Designation).filter(
        Designation.id == employee.designation_id
    ).first()

    # Leave Balance
    leave_balance = db.query(LeaveBalance.remaining_days).filter(
        LeaveBalance.employee_id == employee_id
    ).scalar()

    # Leaves Taken
    leaves_taken = db.query(func.count(LeaveRequest.id)).filter(
        LeaveRequest.employee_id == employee_id,
        LeaveRequest.status == "Approved"
    ).scalar()

    # Pending Requests
    pending_requests = db.query(func.count(LeaveRequest.id)).filter(
        LeaveRequest.employee_id == employee_id,
        LeaveRequest.status == "Pending"
    ).scalar()

    # Next Holiday
    next_holiday = db.query(Holiday)\
        .filter(Holiday.holiday_date >= today)\
        .order_by(Holiday.holiday_date.asc())\
        .first()

    # Recent Leaves
    recent_leaves = db.query(LeaveRequest)\
        .filter(LeaveRequest.employee_id == employee_id)\
        .order_by(LeaveRequest.start_date.desc())\
        .limit(5)\
        .all()

    leave_requests = []

    for leave in recent_leaves:
        leave_requests.append({
            "start_date": leave.start_date,
            "end_date": leave.end_date,
            "leave_type": leave.leave_type,
            "reason": leave.reason,
            "status": leave.status
        })

    return {
        "employee": {
            "name": employee.name,
            "employee_code": employee.employee_code,
            "designation": designation.name
        },
        "cards": {
            "leave_balance": leave_balance,
            "leaves_taken": leaves_taken,
            "pending_requests": pending_requests,
            "next_holiday": {
                "name": next_holiday.name if next_holiday else None,
                "date": next_holiday.holiday_date if next_holiday else None
            }
        },
        "recent_leave_requests": leave_requests
    }

def get_employee_profile(employee_id: int, db: Session):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        return {"error": "Employee not found"}

    designation = db.query(Designation).filter(
        Designation.id == employee.designation_id
    ).first()

    department = db.query(Department).filter(
        Department.id == employee.department_id
    ).first()

    financial = db.query(EmployeeFinancial).filter(
        EmployeeFinancialDetail.employee_id == employee_id
    ).first()

    assets = db.query(EmployeeAsset).filter(
        EmployeeAsset.employee_id == employee_id
    ).first()

    payslips = db.query(Payroll).filter(
        Payroll.employee_id == employee_id
    ).order_by(Payroll.salary_month.desc()).all()

    payslip_list = []

    for pay in payslips:
        payslip_list.append({
            "month": pay.salary_month,
            "salary": pay.net_salary,
            "payslip_file": pay.payslip_file
        })

    return {

        "employee": {
            "name": employee.name,
            "employee_code": employee.employee_code,
            "designation": designation.name if designation else None,
            "department": department.name if department else None,
            "phone": employee.phone_number,
            "address": employee.address,
            "company_email": employee.company_email,
            "personal_email": employee.personal_email
        },

        "financial_details": {
            "bank_account": financial.bank_account_number if financial else None,
            "pan_number": financial.pan_number if financial else None,
            "uan_number": financial.uan_pf_number if financial else None
        },

        "assets": {
            "access_card": assets.access_card_number if assets else None,
            "laptop_asset": assets.laptop_asset_id if assets else None,
            "additional_assets": assets.additional_assets if assets else None
        },

        "payslips": payslip_list
    }