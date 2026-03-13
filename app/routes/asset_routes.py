from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.asset_schema import AssetCreate, AssetUpdate
from app.controllers.asset_controller import (
    assign_asset,
    get_all_assets,
    get_asset_by_employee,
    update_asset,
    return_asset,
    delete_asset
)

from app.database.database import get_db

router = APIRouter(
    prefix="/admin",
    tags=["Assets Management"]
)


@router.post("/assets")
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    return assign_asset(db, asset)


@router.get("/assets")
def list_assets(db: Session = Depends(get_db)):
    return get_all_assets(db)


@router.get("/employee/{employee_id}")
def get_employee_asset(employee_id: int, db: Session = Depends(get_db)):
    return get_asset_by_employee(db, employee_id)


@router.put("/{asset_id}")
def update_asset_api(asset_id: int, asset: AssetUpdate, db: Session = Depends(get_db)):
    return update_asset(db, asset_id, asset)


@router.put("/return/{asset_id}")
def return_asset_api(asset_id: int, db: Session = Depends(get_db)):
    return return_asset(db, asset_id)


@router.delete("/{asset_id}")
def delete_asset_api(asset_id: int, db: Session = Depends(get_db)):
    return delete_asset(db, asset_id)