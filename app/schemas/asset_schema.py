from pydantic import BaseModel


class AssetCreate(BaseModel):
    employee_id: int
    laptop_asset_id: str
    access_card: str
    additional_asset: str


class AssetUpdate(BaseModel):
    laptop_asset_id: str
    access_card: str
    additional_asset: str
    status: str