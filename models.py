# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scheme_code = Column(String, nullable=False)
    units = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)
    current_value = Column(Float, default=0.0)
    # SQLite handles datetime slightly differently, but this still works
    last_updated = Column(DateTime, server_default=func.now())