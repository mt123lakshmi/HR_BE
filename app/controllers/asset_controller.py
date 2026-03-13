from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.models import Asset, Employee


# Helper function (avoid repeating logic)
def get_asset_or_404(db: Session, asset_id: int):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    return asset


# Assign Asset
def assign_asset(db: Session, asset):

    # Check employee exists
    employee = db.query(Employee).filter(Employee.id == asset.employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Prevent assigning multiple assets to same employee
    existing_employee_asset = db.query(Asset).filter(
        Asset.employee_id == asset.employee_id,
        Asset.status == "Assigned"
    ).first()

    if existing_employee_asset:
        raise HTTPException(
            status_code=400,
            detail="Employee already has an assigned asset"
        )

    # Prevent duplicate laptop asset id
    existing_laptop = db.query(Asset).filter(
        Asset.laptop_asset_id == asset.laptop_asset_id
    ).first()

    if existing_laptop:
        raise HTTPException(
            status_code=400,
            detail="Laptop asset ID already exists"
        )

    new_asset = Asset(
        employee_id=asset.employee_id,
        laptop_asset_id=asset.laptop_asset_id,
        access_card=asset.access_card,
        additional_asset=asset.additional_asset,
        status="Assigned"
    )

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    return new_asset


# Get All Assets
def get_all_assets(db: Session):

    assets = db.query(Asset).order_by(Asset.id.desc()).all()

    return assets


# Get Asset by Employee
def get_asset_by_employee(db: Session, employee_id: int):

    asset = db.query(Asset).filter(
        Asset.employee_id == employee_id
    ).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found for employee")

    return asset


# Update Asset
def update_asset(db: Session, asset_id: int, data):

    asset = get_asset_or_404(db, asset_id)

    # Check duplicate laptop id (if changed)
    duplicate_laptop = db.query(Asset).filter(
        Asset.laptop_asset_id == data.laptop_asset_id,
        Asset.id != asset_id
    ).first()

    if duplicate_laptop:
        raise HTTPException(
            status_code=400,
            detail="Laptop asset ID already exists"
        )

    asset.laptop_asset_id = data.laptop_asset_id
    asset.access_card = data.access_card
    asset.additional_asset = data.additional_asset
    asset.status = data.status

    db.commit()
    db.refresh(asset)

    return asset


# Return Asset
def return_asset(db: Session, asset_id: int):

    asset = get_asset_or_404(db, asset_id)

    if asset.status == "Returned":
        raise HTTPException(
            status_code=400,
            detail="Asset already returned"
        )

    asset.status = "Returned"

    db.commit()
    db.refresh(asset)

    return {"message": "Asset returned successfully"}


# Delete Asset
def delete_asset(db: Session, asset_id: int):

    asset = get_asset_or_404(db, asset_id)

    db.delete(asset)
    db.commit()

    return {"message": "Asset deleted successfully"}