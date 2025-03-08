# services/fund_service.py
import requests
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "latest-mutual-fund-nav.p.rapidapi.com"


class FundService:
    @staticmethod
    async def get_fund_master_data():
        url = f"https://{RAPIDAPI_HOST}/master"
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        }
        querystring = {"RTA_Agent_Code": "CAMS"}

        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch fund data")
        return response.json()

    @staticmethod
    async def get_schemes_by_fund_house(fund_house: str):
        url = f"https://{RAPIDAPI_HOST}/master"
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        }
        querystring = {"RTA_Agent_Code": "CAMS"}

        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch schemes")

        # Filter schemes by fund house
        all_schemes = response.json()
        filtered_schemes = [
            scheme for scheme in all_schemes
            if scheme.get('Fund_House', '').lower() == fund_house.lower()
        ]
        return filtered_schemes

    @staticmethod
    async def get_current_nav(scheme_code: str):
        url = f"https://{RAPIDAPI_HOST}/master"
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        }
        querystring = {"RTA_Agent_Code": "CAMS"}

        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch NAV")

        schemes = response.json()
        for scheme in schemes:
            if scheme.get('Scheme_Code') == scheme_code:
                return float(scheme.get('Net_Asset_Value', 0))
        raise HTTPException(status_code=404, detail="Scheme not found")