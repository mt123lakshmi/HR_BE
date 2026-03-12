from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.admin_schema import EmployeeCreate,EmployeeUpdate,DepartmentCreate,DesignationCreate,EmployeeStatusUpdate
from app.database.database import get_db
from app.controllers.admin_controller import get_admin_dashboard,get_employees,get_employee_profile,create_employee,get_departments,get_designations,update_employee,delete_employee,create_department,create_designation,update_employee_status,get_employee_documents,get_employee_assets,get_assets
from app.schemas.admin_schema import AdminDashboardResponse


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard", response_model=AdminDashboardResponse)
def admin_dashboard(db: Session = Depends(get_db)):

    return get_admin_dashboard(db)

@router.get("/employees")
def get_admin_employees(db: Session = Depends(get_db)):

    return get_employees(db)

@router.get("/employees/{employee_id}")
def get_employee_profile_route(
        employee_id: int,
        db: Session = Depends(get_db)
):

    return get_employee_profile(employee_id, db)

@router.post("/employees")
def add_employee(
        data: EmployeeCreate,
        db: Session = Depends(get_db)
):

    return create_employee(data, db)

@router.get("/departments")
def get_all_departments(db: Session = Depends(get_db)):

    return get_departments(db)
@router.get("/designations")
def get_all_designations(db: Session = Depends(get_db)):

    return get_designations(db)

@router.put("/employees/{employee_id}")
def edit_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db)
):

    return update_employee(employee_id, data, db)

@router.delete("/employees/{employee_id}")
def remove_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    return delete_employee(employee_id, db)

@router.post("/departments")
def add_department(
    data: DepartmentCreate,
    db: Session = Depends(get_db)
):
    return create_department(data, db)

@router.post("/designations")
def add_designation(
    data: DesignationCreate,
    db: Session = Depends(get_db)
):
    return create_designation(data, db)

@router.get("/employees")
def get_admin_employees(
    search: str = None,
    db: Session = Depends(get_db)
):

    return get_employees(db, search)

@router.get("/employees")
def get_admin_employees(
    search: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    return get_employees(db, search, page, limit)

@router.get("/employees")
def get_admin_employees(
    search: str = None,
    department_id: int = None,
    designation_id: int = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    return get_employees(
        db,
        search,
        page,
        limit,
        department_id,
        designation_id
    )

@router.patch("/employees/{employee_id}/status")
def change_employee_status(
    employee_id: int,
    data: EmployeeStatusUpdate,
    db: Session = Depends(get_db)
):

    return update_employee_status(employee_id, data, db)

@router.get("/employees/{employee_id}/documents")
def view_employee_documents(
    employee_id: int,
    db: Session = Depends(get_db)
):

    return get_employee_documents(employee_id, db)

@router.get("/employees/{employee_id}/assets")
def view_employee_assets(
    employee_id: int,
    db: Session = Depends(get_db)
):

    return get_employee_assets(employee_id, db)

@router.get("/assets")
def view_assets(db: Session = Depends(get_db)):

    return get_assets(db)