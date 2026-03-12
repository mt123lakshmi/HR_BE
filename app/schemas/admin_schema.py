from pydantic import BaseModel
from datetime import date
from typing import Optional


class PendingLeaveResponse(BaseModel):
    employee_name: str
    leave_type: str
    start_date: date
    end_date: date
    reason: str
    status: str


class AdminDashboardResponse(BaseModel):
    total_employees: int
    leaves_pending: int
    on_leave_today: int
    upcoming_holidays: int
    pending_leave_requests: list[PendingLeaveResponse]

class EmployeeListResponse(BaseModel):

    id: int
    name: str
    company_email: str
    employee_code: str
    department: str
    role: str

class EmployeeCreate(BaseModel):

    # Personal Details
    employee_code: str
    name: str
    phone_number: str
    department_id: int
    designation_id: int
    address: str
    company_email: str
    personal_email: str

    # Financial
    bank_account_number: Optional[str]
    pan_number: Optional[str]
    uan_pf_number: Optional[str]

    # Assets
    access_card_number: Optional[str]
    laptop_asset_id: Optional[str]
    additional_assets: Optional[str]

    # Documents
    pan_card: Optional[str]
    aadhaar_card: Optional[str]
    ssc_certificate: Optional[str]
    inter_certificate: Optional[str]
    btech_certificate: Optional[str]


class EmployeeUpdate(BaseModel):

    name: str
    phone_number: str
    department_id: int
    designation_id: int
    address: str
    company_email: str
    personal_email: str

class DepartmentCreate(BaseModel):
    name: str

class DesignationCreate(BaseModel):
    name: str

class EmployeeStatusUpdate(BaseModel):
    employment_status: str