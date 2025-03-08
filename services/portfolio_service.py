# services/portfolio_service.py
from sqlalchemy.orm import Session
from models import Portfolio
from services.fund_service import FundService
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


class PortfolioService:
    scheduler = BackgroundScheduler()

    @staticmethod
    def update_portfolio_values(db: Session):
        portfolios = db.query(Portfolio).all()
        for portfolio in portfolios:
            try:
                current_nav = FundService.get_current_nav(portfolio.scheme_code)
                portfolio.current_value = portfolio.units * current_nav
                portfolio.last_updated = datetime.utcnow()
            except Exception as e:
                print(f"Error updating portfolio {portfolio.id}: {str(e)}")
        db.commit()

    @classmethod
    def start_scheduler(cls, db: Session):
        if not cls.scheduler.running:
            cls.scheduler.add_job(
                cls.update_portfolio_values,
                'interval',
                hours=1,
                args=[db]
            )
            cls.scheduler.start()