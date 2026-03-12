from sqlalchemy.orm import Session
from app.models.models import LeaveRequest


def get_leave_requests(db: Session):

    leaves = db.query(LeaveRequest).all()

    result = []

    for leave in leaves:
        result.append({
            "leave_id": leave.id,
            "employee_name": leave.employee.name if leave.employee else None,
            "leave_type": leave.leave_type,
            "start_date": leave.start_date,
            "end_date": leave.end_date,
            "reason": leave.reason,
            "status": leave.status
        })

    return result


def approve_leave(leave_id: int, db: Session):

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        return {"error": "Leave request not found"}

    if leave.status != "Pending":
        return {"error": "Leave already processed"}

    # approve leave
    leave.status = "Approved"
    leave.approved_at = datetime.utcnow()

    # update leave balance
    leave_balance = db.query(LeaveBalance).filter(
        LeaveBalance.employee_id == leave.employee_id
    ).first()

    if leave_balance:

        if leave.leave_type == "Casual":
            leave_balance.casual_leave_used += leave.total_days
            leave_balance.casual_leave_remaining -= leave.total_days

        elif leave.leave_type == "Sick":
            leave_balance.sick_leave_used += leave.total_days
            leave_balance.sick_leave_remaining -= leave.total_days

        elif leave.leave_type == "Earned":
            leave_balance.earned_leave_used += leave.total_days
            leave_balance.earned_leave_remaining -= leave.total_days

    db.commit()

    return {
        "message": "Leave approved successfully"
    }


def reject_leave(leave_id: int, rejection_reason: str, db: Session):

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        return {"error": "Leave request not found"}

    if leave.status != "Pending":
        return {"error": "Leave already processed"}

    leave.status = "Rejected"
    leave.rejection_reason = rejection_reason

    db.commit()

    return {
        "message": "Leave rejected successfully",
        "reason": rejection_reason
    }