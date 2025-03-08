# schemas.py
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class FundScheme(BaseModel):
    Scheme_Code: str
    Scheme_Name: str
    Fund_House: str
    Net_Asset_Value: float
    Date: str  # Assuming the API returns a date

    class Config:
        from_attributes = True


class PortfolioCreate(BaseModel):
    scheme_code: str
    units: float
    purchase_price: float


class PortfolioResponse(BaseModel):
    id: int
    scheme_code: str
    units: float
    purchase_price: float
    current_value: float
    last_updated: datetime
    scheme_name: str = None
    fund_house: str = None

    class Config:
        from_attributes = True