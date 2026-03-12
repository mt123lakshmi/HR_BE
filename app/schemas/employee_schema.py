from pydantic import BaseModel
from typing import List, Optional


class PersonalDetails(BaseModel):
    employee_code: str
    name: str
    mobile: str
    role: str
    department: str
    address: str
    company_email: str
    personal_email: str


class FinancialDetails(BaseModel):
    bank_account: Optional[str]
    pan_number: Optional[str]
    uan_number: Optional[str]


class AssetDetails(BaseModel):
    access_card: Optional[str]
    laptop_asset_id: Optional[str]
    additional_assets: Optional[str]


class PayslipDetails(BaseModel):
    month: str
    year: int
    payslip_url: Optional[str]


class EmployeeProfileResponse(BaseModel):
    personal_details: PersonalDetails
    financial_details: FinancialDetails
    assets: AssetDetails
    payslips: List[PayslipDetails]