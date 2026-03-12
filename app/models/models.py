from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, DECIMAL, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), unique=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class Designation(Base):
    __tablename__ = "designations"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    department_id = Column(Integer, ForeignKey("departments.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

    employee_code = Column(String(20), unique=True)

    name = Column(String(100), nullable=False)

    company_email = Column(String(150), unique=True)
    personal_email = Column(String(150))

    phone_number = Column(String(20))

    department_id = Column(Integer, ForeignKey("departments.id"))
    designation_id = Column(Integer, ForeignKey("designations.id"))

    joining_date = Column(Date)

    salary = Column(DECIMAL(10, 2))

    date_of_birth = Column(Date)

    emergency_contact = Column(String(20))

    address = Column(Text)

    profile_photo = Column(String(255))

    employment_status = Column(String(50), default="Active")

    resignation_date = Column(Date)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(150), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    role = Column(String(50), nullable=False)

    employee_id = Column(Integer, ForeignKey("employees.id"))

    is_active = Column(Integer, default=1)

    last_login = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, ForeignKey("employees.id"))

    attendance_date = Column(Date)

    check_in_time = Column(DateTime)

    check_out_time = Column(DateTime)

    status = Column(String(50))

    late_entry = Column(Integer, default=0)

    work_hours = Column(DECIMAL(5,2))

    overtime_hours = Column(DECIMAL(5,2))

    remarks = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, ForeignKey("employees.id"))

    employee = relationship("Employee")

    leave_type = Column(String(50))

    start_date = Column(Date)

    end_date = Column(Date)

    total_days = Column(Integer)

    reason = Column(Text)

    status = Column(String(50), default="Pending")

    applied_date = Column(DateTime, default=datetime.utcnow)

    approved_by = Column(Integer, ForeignKey("users.id"))

    approved_at = Column(DateTime)
    rejection_reason = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class LeaveBalance(Base):
    __tablename__ = "leave_balances"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, ForeignKey("employees.id"))

    leave_year = Column(Integer)

    casual_leave_total = Column(Integer, default=0)
    casual_leave_used = Column(Integer, default=0)
    casual_leave_remaining = Column(Integer, default=0)

    sick_leave_total = Column(Integer, default=0)
    sick_leave_used = Column(Integer, default=0)
    sick_leave_remaining = Column(Integer, default=0)

    earned_leave_total = Column(Integer, default=0)
    earned_leave_used = Column(Integer, default=0)
    earned_leave_remaining = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class Payroll(Base):
    __tablename__ = "payroll"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, ForeignKey("employees.id"))

    basic_salary = Column(DECIMAL(10,2))

    hra = Column(DECIMAL(10,2))

    allowances = Column(DECIMAL(10,2))

    deductions = Column(DECIMAL(10,2))

    net_salary = Column(DECIMAL(10,2))

    payroll_month = Column(String(20))

    payroll_year = Column(Integer)

    payslip_file = Column(String(255))

    generated_at = Column(DateTime, default=datetime.utcnow)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, ForeignKey("employees.id"))

    title = Column(String(200))

    message = Column(Text)

    is_read = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class Resignation(Base):
    __tablename__ = "resignations"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, ForeignKey("employees.id"))

    reason = Column(Text)

    requested_date = Column(Date)

    last_working_day = Column(Date)

    status = Column(String(50), default="Pending")

    approved_by = Column(Integer, ForeignKey("users.id"))

    approved_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)

    asset_code = Column(String(50), unique=True)

    asset_name = Column(String(100))

    asset_type = Column(String(100))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


class EmployeeAsset(Base):
    __tablename__ = "employee_assets"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, ForeignKey("employees.id"))

    asset_id = Column(Integer, ForeignKey("assets.id"))

    assigned_date = Column(Date)

    returned_date = Column(Date)

    status = Column(String(50), default="Assigned")

    created_at = Column(DateTime, default=datetime.utcnow)

class EmployeeFinancialDetail(Base):
    __tablename__ = "employee_financial_details"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, ForeignKey("employees.id"))

    bank_account_number = Column(String(50))

    bank_name = Column(String(100))

    ifsc_code = Column(String(20))

    pan_number = Column(String(20))

    uan_pf_number = Column(String(50))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class Holiday(Base):
    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150))

    holiday_date = Column(Date)

    description = Column(Text)

    created_by = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class EmployeeDocument(Base):
    __tablename__ = "employee_documents"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, ForeignKey("employees.id"))

    document_type = Column(String(100))

    document_file = Column(String(255))

    uploaded_at = Column(DateTime, default=datetime.utcnow)