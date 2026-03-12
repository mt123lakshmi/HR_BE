from sqlalchemy.orm import Session
from sqlalchemy import func,or_

from datetime import date

from app.models.models import Employee, LeaveRequest, Holiday, Department, Designation, EmployeeFinancialDetail,EmployeeAsset, EmployeeDocument
    


def get_admin_dashboard(db: Session):

    today = date.today()

    # Total Employees
    total_employees = db.query(func.count(Employee.id)).scalar()

    # Pending Leaves
    leaves_pending = (
        db.query(func.count(LeaveRequest.id))
        .filter(LeaveRequest.status == "Pending")
        .scalar()
    )

    # On Leave Today
    on_leave_today = (
        db.query(func.count(LeaveRequest.id))
        .filter(
            LeaveRequest.start_date <= today,
            LeaveRequest.end_date >= today,
            LeaveRequest.status == "Approved"
        )
        .scalar()
    )

    # Upcoming Holidays
    upcoming_holidays = (
        db.query(func.count(Holiday.id))
        .filter(Holiday.holiday_date >= today)
        .scalar()
    )

    # Pending Leave Requests
    pending_leaves = (
        db.query(LeaveRequest)
        .filter(LeaveRequest.status == "Pending")
        .all()
    )

    pending_leave_requests = []

    for leave in pending_leaves:
        pending_leave_requests.append({
            "employee_name": leave.employee.name,
            "leave_type": leave.leave_type,
            "start_date": leave.start_date,
            "end_date": leave.end_date,
            "reason": leave.reason,
            "status": leave.status
        })

    return {
        "total_employees": total_employees,
        "leaves_pending": leaves_pending,
        "on_leave_today": on_leave_today,
        "upcoming_holidays": upcoming_holidays,
        "pending_leave_requests": pending_leave_requests
    }


def get_employees(db: Session):

    employees = (
        db.query(
            Employee.id,
            Employee.name,
            Employee.company_email,
            Employee.employee_code,
            Department.name.label("department"),
            Designation.name.label("role")
        )
        .join(Department, Employee.department_id == Department.id)
        .join(Designation, Employee.designation_id == Designation.id)
        .all()
    )

    result = []

    for emp in employees:
        result.append({
            "id": emp.id,
            "name": emp.name,
            "company_email": emp.company_email,
            "employee_code": emp.employee_code,
            "department": emp.department,
            "role": emp.role
        })

    return result

from app.models.models import EmployeeFinancialDetail, EmployeeAsset, Asset, EmployeeDocument


def get_employee_profile(employee_id: int, db: Session):

    employee = (
        db.query(
            Employee.id,
            Employee.employee_code,
            Employee.name,
            Employee.phone_number,
            Employee.address,
            Employee.company_email,
            Employee.personal_email,
            Department.name.label("department"),
            Designation.name.label("role")
        )
        .join(Department, Employee.department_id == Department.id)
        .join(Designation, Employee.designation_id == Designation.id)
        .filter(Employee.id == employee_id)
        .first()
    )

    financial = (
        db.query(EmployeeFinancialDetail)
        .filter(EmployeeFinancialDetail.employee_id == employee_id)
        .first()
    )

    assets = (
        db.query(Asset.asset_name, Asset.asset_code)
        .join(EmployeeAsset, Asset.id == EmployeeAsset.asset_id)
        .filter(EmployeeAsset.employee_id == employee_id)
        .all()
    )

    documents = (
        db.query(EmployeeDocument.document_type, EmployeeDocument.document_file)
        .filter(EmployeeDocument.employee_id == employee_id)
        .all()
    )

    return {
        "employee": employee,
        "financial_details": financial,
        "assets": assets,
        "documents": documents
    }
def create_employee(data, db: Session):

    # --------------------
    # Create Employee
    # --------------------

    employee = Employee(
        employee_code=data.employee_code,
        name=data.name,
        phone_number=data.phone_number,
        department_id=data.department_id,
        designation_id=data.designation_id,
        address=data.address,
        company_email=data.company_email,
        personal_email=data.personal_email
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    # --------------------
    # Financial Details
    # --------------------

    financial = EmployeeFinancialDetail(
        employee_id=employee.id,
        bank_account_number=data.bank_account_number,
        pan_number=data.pan_number,
        uan_pf_number=data.uan_pf_number
    )

    db.add(financial)

    # --------------------
    # Asset Management
    # --------------------

    asset = EmployeeAsset(
        employee_id=employee.id,
        access_card_number=data.access_card_number,
        laptop_asset_id=data.laptop_asset_id,
        additional_assets=data.additional_assets
    )

    db.add(asset)

    # --------------------
    # Documents
    # --------------------

    documents = [

        EmployeeDocument(
            employee_id=employee.id,
            document_type="PAN Card",
            document_file=data.pan_card
        ),

        EmployeeDocument(
            employee_id=employee.id,
            document_type="Aadhaar Card",
            document_file=data.aadhaar_card
        ),

        EmployeeDocument(
            employee_id=employee.id,
            document_type="SSC Certificate",
            document_file=data.ssc_certificate
        ),

        EmployeeDocument(
            employee_id=employee.id,
            document_type="Inter Certificate",
            document_file=data.inter_certificate
        ),

        EmployeeDocument(
            employee_id=employee.id,
            document_type="BTech Certificate",
            document_file=data.btech_certificate
        )

    ]

    for doc in documents:
        if doc.document_file:
            db.add(doc)

    db.commit()

    return {
        "message": "Employee created successfully",
        "employee_id": employee.id
    }

def get_departments(db: Session):

    departments = db.query(Department).all()

    result = []

    for dept in departments:
        result.append({
            "id": dept.id,
            "name": dept.name
        })

    return result

def get_designations(db: Session):

    designations = db.query(Designation).all()

    result = []

    for des in designations:
        result.append({
            "id": des.id,
            "name": des.name,
            "department_id": des.department_id
        })

    return result

def update_employee(employee_id: int, data, db: Session):

    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        return {"message": "Employee not found"}

    employee.name = data.name
    employee.phone_number = data.phone_number
    employee.department_id = data.department_id
    employee.designation_id = data.designation_id
    employee.address = data.address
    employee.company_email = data.company_email
    employee.personal_email = data.personal_email

    db.commit()
    db.refresh(employee)

    return {
        "message": "Employee updated successfully",
        "employee_id": employee.id
    }

def delete_employee(employee_id: int, db: Session):

    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        return {"message": "Employee not found"}

    db.delete(employee)
    db.commit()

    return {
        "message": "Employee deleted successfully"
    }

def create_department(data, db: Session):

    department = Department(
        name=data.name
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    return {
        "message": "Department created successfully",
        "department_id": department.id
    }
def create_designation(data, db: Session):

    designation = Designation(
        name=data.name
    )

    db.add(designation)
    db.commit()
    db.refresh(designation)

    return {
        "message": "Designation created successfully",
        "designation_id": designation.id
    }
def get_employees(db: Session, search: str = None):

    query = db.query(
        Employee.id,
        Employee.name,
        Employee.company_email,
        Employee.employee_code,
        Department.name.label("department"),
        Designation.name.label("role")
    ).join(
        Department, Employee.department_id == Department.id
    ).join(
        Designation, Employee.designation_id == Designation.id
    )

    if search:
        query = query.filter(
            or_(
                Employee.name.ilike(f"%{search}%"),
                Employee.company_email.ilike(f"%{search}%"),
                Employee.employee_code.ilike(f"%{search}%")
            )
        )

    employees = query.all()

    result = []

    for emp in employees:
        result.append({
            "id": emp.id,
            "name": emp.name,
            "company_email": emp.company_email,
            "employee_code": emp.employee_code,
            "department": emp.department,
            "role": emp.role
        })

    return result

def get_employees(db: Session, search: str = None, page: int = 1, limit: int = 10):

    query = db.query(
        Employee.id,
        Employee.name,
        Employee.company_email,
        Employee.employee_code,
        Department.name.label("department"),
        Designation.name.label("role")
    ).join(
        Department, Employee.department_id == Department.id
    ).join(
        Designation, Employee.designation_id == Designation.id
    )

    if search:
        query = query.filter(
            or_(
                Employee.name.ilike(f"%{search}%"),
                Employee.company_email.ilike(f"%{search}%"),
                Employee.employee_code.ilike(f"%{search}%")
            )
        )

    total = query.count()

    employees = query.offset((page - 1) * limit).limit(limit).all()

    result = []

    for emp in employees:
        result.append({
            "id": emp.id,
            "name": emp.name,
            "company_email": emp.company_email,
            "employee_code": emp.employee_code,
            "department": emp.department,
            "role": emp.role
        })

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "employees": result
    }

def update_employee_status(employee_id: int, data, db: Session):

    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        return {"message": "Employee not found"}

    employee.employment_status = data.employment_status

    db.commit()
    db.refresh(employee)

    return {
        "message": "Employee status updated successfully",
        "employee_id": employee.id,
        "employment_status": employee.employment_status
    }

def get_employee_documents(employee_id: int, db: Session):

    documents = db.query(EmployeeDocument).filter(
        EmployeeDocument.employee_id == employee_id
    ).all()

    result = []

    for doc in documents:
        result.append({
            "document_type": doc.document_type,
            "document_file": doc.document_file
        })

    return result

def get_employee_assets(employee_id: int, db: Session):

    assets = db.query(
        Asset.asset_name,
        Asset.asset_code
    ).join(
        EmployeeAsset,
        Asset.id == EmployeeAsset.asset_id
    ).filter(
        EmployeeAsset.employee_id == employee_id
    ).all()

    result = []

    for asset in assets:
        result.append({
            "asset_name": asset.asset_name,
            "asset_code": asset.asset_code
        })

    return result

def get_assets(db: Session):

    assets = db.query(Asset).all()

    result = []

    for asset in assets:
        result.append({
            "id": asset.id,
            "asset_name": asset.asset_name,
            "asset_code": asset.asset_code
        })

    return result