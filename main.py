# main.py
from fastapi import FastAPI
from routers import auth, funds, portfolio
from database import engine, get_db
import models
from services.portfolio_service import PortfolioService
import uvicorn

app = FastAPI(
    title="Mutual Fund Brokerage API",
    description="API for managing mutual fund investments",
    version="1.0.0"
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(funds.router)
app.include_router(portfolio.router)

# Start portfolio update scheduler
@app.on_event("startup")
def startup_event():
    db = next(get_db())
    PortfolioService.start_scheduler(db)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)