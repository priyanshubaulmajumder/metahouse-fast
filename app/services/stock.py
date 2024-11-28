from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func, and_
from typing import List, Optional, Dict, Any, Tuple
from datetime import date, datetime
from app.models.stock import Stock, StockWCategoryMapping
from app.schemas.stock import StockResponse, StockFundamentalsResponse, ShareHoldingPatternResponse, FinancialsOverviewResponse, DetailedFinancialsResponse
from app.core.config import settings
from app.utils.constants import ExchangeChoices
#from app.utils.cache import cache
from app.utils.helpers import get_decimal
#from app.services.modal_generic_service import ModalGenericService
from app.services.response_data_process_service import ResponseDataProcessService
from app.services.stock_hist import StockHistPriceService

class StockService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.hist_service = StockHistPriceService(db)

    @staticmethod
    async def search_stocks(db: AsyncSession, search_text: str, skip: int = 0, limit: int = 10):
        if not search_text:
            return [], 0
        
        search_list = search_text.split(' ')
        search_pattern = r".*".join(search_list)

        query = select(Stock).filter(
            or_(
                Stock.name.op('~*')(search_pattern),
                Stock.bse_symbol.op('~*')(search_pattern),
                Stock.nse_symbol.op('~*')(search_pattern)
            )
        )
        
        total = await db.scalar(select(func.count()).select_from(query.subquery()))
        result = await db.execute(query.offset(skip).limit(limit))
        stocks = result.scalars().all()
        return stocks, total

    async def get_stock_historical_price(self, id_type: str, id_value: str, exchange: str, start_date: str, end_date: str):
        stock = await self._get_stock_by_id(id_type, id_value)
        if not stock:
            return []
        
        return await self.hist_service.get_hist_prices_for_wstockcode(
            self.db, exchange, stock.wstockcode, start_date, end_date
        )

    @staticmethod
    async def get_stock_market_news(db: AsyncSession, news_type: str):
        # This method would typically call an external news API or service
        # For demonstration, we'll return a placeholder
        return [{"title": "Sample News", "content": "This is a sample news item."}]

    @staticmethod
    async def get_stock_market_specific_news(db: AsyncSession, news_id: str):
        # This method would typically call an external news API or service
        # For demonstration, we'll return a placeholder
        return {"id": news_id, "title": "Specific News", "content": "This is a specific news item."}

    @staticmethod
    async def get_etfs(db: AsyncSession, fund_types: List[str]):
        query = select(Stock).filter(Stock.instrument_type.in_(fund_types))
        result = await db.execute(query)
        return result.scalars().all()

    async def get_similar_etfs(self, id_type: str, id_value: str):
        stock = await self._get_stock_by_id(id_type, id_value)
        if not stock or stock.category.lower() != "etfs fund":
            return []
        
        query = select(Stock).filter(
            Stock.category == "etfs fund",
            Stock.sector == stock.sector
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_stock_indices_for_category(db: AsyncSession, category: str):
        query = select(StockWCategoryMapping).filter(StockWCategoryMapping.category == category)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_index_wise_stocks(self, id_type: str, id_value: str, skip: int = 0, limit: int = 500):
        index = await self._get_stock_by_id(id_type, id_value)
        if not index:
            return [], 0
        
        query = select(Stock).filter(Stock.sector == index.sector)
        total = await self.db.scalar(select(func.count()).select_from(query.subquery()))
        result = await self.db.execute(query.offset(skip).limit(limit))
        stocks = result.scalars().all()
        return stocks, total

    async def get_stock_fundamentals(self, id_type: str, id_value: str, exchange: str):
        stock = await self._get_stock_by_id(id_type, id_value)
        if not stock:
            return None
        
        # Here you would typically fetch and return the fundamental data
        # For demonstration, we'll return a placeholder
        return StockFundamentalsResponse(pe=get_decimal(15.5), pb=get_decimal(2.3), dividend_yield=get_decimal(1.5))

    async def get_latest_share_holding_pattern(self, id_type: str, id_value: str, entity: str):
        stock = await self._get_stock_by_id(id_type, id_value)
        if not stock:
            return None
        
        # Here you would typically fetch and return the shareholding pattern
        # For demonstration, we'll return a placeholder
        return ShareHoldingPatternResponse(promoters=45.5, fii=25.3, dii=15.2, public=14.0)

    async def get_financial_data_overview(self, id_type: str, id_value: str, fdata: str, period: str, rtype: str):
        stock = await self._get_stock_by_id(id_type, id_value)
        if not stock:
            return None
        
        # Here you would typically fetch and return the financial data overview
        # For demonstration, we'll return a placeholder
        return FinancialsOverviewResponse(revenue=1000000, expenses=800000, profit_loss=200000)

    async def get_financial_data_detailed(self, id_type: str, id_value: str, period: str, rtype: str):
        stock = await self._get_stock_by_id(id_type, id_value)
        if not stock:
            return None
        
        # Here you would typically fetch and return the detailed financial data
        # For demonstration, we'll return a placeholder
        return DetailedFinancialsResponse(
            balance_sheet={"assets": 5000000, "liabilities": 3000000},
            profit_loss={"revenue": 1000000, "expenses": 800000},
            cash_flow={"operating": 300000, "investing": -100000, "financing": -50000}
        )

    async def _get_stock_by_id(self, id_type: str, id_value: str) -> Optional[Stock]:
        if id_type == 'wstockcode':
            query = select(Stock).filter(Stock.wstockcode == id_value)
        elif id_type == 'isin':
            query = select(Stock).filter(Stock.isin == id_value)
        elif id_type == 'nse_symbol':
            query = select(Stock).filter(Stock.nse_symbol == id_value)
        elif id_type == 'bse_symbol':
            query = select(Stock).filter(Stock.bse_symbol == id_value)
        else:
            return None
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_stock_technical_indicators(self, id_type: str, id_value: str):
        stock = await self._get_stock_by_id(id_type, id_value)
        if not stock:
            return None
        
        return {
            "rsi": stock.rsi,
            "macd": stock.macd,
            "ema": stock.ema,
            "sma": stock.sma,
            "std": stock.std
        }

    async def get_stock_returns(self, id_type: str, id_value: str):
        stock = await self._get_stock_by_id(id_type, id_value)
        if not stock:
            return None
        
        return {
            "one_month": stock.returns_one_month,
            "three_months": stock.returns_three_months,
            "six_months": stock.returns_six_months,
            "one_year": stock.returns_one_year,
            "two_years": stock.returns_two_years,
            "three_years": stock.returns_three_years,
            "five_years": stock.returns_five_years
        }

