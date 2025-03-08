# routers/funds.py
from fastapi import APIRouter, Depends
from services.fund_service import FundService
from schemas import FundScheme
from typing import List

router = APIRouter(prefix="/funds", tags=["funds"])

@router.get("/master", response_model=List[FundScheme])
async def get_all_funds():
    return await FundService.get_fund_master_data()

@router.get("/schemes/{fund_house}", response_model=List[FundScheme])
async def get_schemes(fund_house: str):
    return await FundService.get_schemes_by_fund_house(fund_house)