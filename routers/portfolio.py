# routers/portfolio.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import PortfolioCreate, PortfolioResponse
from models import Portfolio, User
from database import get_db
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from utils.auth import SECRET_KEY, ALGORITHM
from typing import List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
router = APIRouter(prefix="/portfolio", tags=["portfolio"])


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user


@router.post("/", response_model=PortfolioResponse)
def create_portfolio(
        portfolio: PortfolioCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    db_portfolio = Portfolio(
        user_id=current_user.id,
        scheme_code=portfolio.scheme_code,
        units=portfolio.units,
        purchase_price=portfolio.purchase_price
    )
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


@router.get("/", response_model=List[PortfolioResponse])
def get_portfolio(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    portfolios = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).all()
    return portfolios