from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.models.screener import Screener, ScreenerInstrument
from app.models.stock import Stock
from app.models.scheme import Scheme
from app.schemas.screener import ScreenerResponse, ScreenerInstrumentResponse, ScreenerWithInstrumentsResponse
from app.schemas.stock import StockResponse
from app.schemas.scheme import SchemeSerializer as SchemeResponse
from typing import List, Optional
from app.core.config import settings
from fastapi import HTTPException
import logging
logger = logging.getLogger(__name__)
#from app.utils.cache import cache

class ScreenerService:
    @staticmethod
    async def get_custom_screener(db: AsyncSession, screener_id: str, instrument_type: str):
        query = select(ScreenerInstrument).filter(ScreenerInstrument.screener == screener_id)
        result = await db.execute(query)
        obj = result.scalar_one_or_none()
        
        if not obj:
            return []
        
        kwargs = dict(instruments=obj.instruments, cols=obj.cols)
        if instrument_type == "stocks":
            return await ScreenerService.get_stocks_custom_screener(db, **kwargs)
        elif instrument_type == "schemes":
            return await ScreenerService.get_schemes_custom_screener(db, **kwargs)
        return []

    @staticmethod
    async def get_screener(db: AsyncSession, screener_id: str):
        """
        Retrieve a screener by its ID.
        """
        try:
            result = await db.execute(
                select(Screener).filter_by(id=screener_id)
            )
            screener = result.scalar_one_or_none()
            if screener is None:
                raise HTTPException(status_code=404, detail="Screener not found")
            return screener
        except Exception as e:
            logger.error(f"Error retrieving Screener for ID: {screener_id} - {e}")
            raise

    @staticmethod
    async def get_screener_by_wpc(db: AsyncSession, screener_wpc: str) -> Optional[ScreenerResponse]:
        result = await db.execute(
            select(Screener).where(Screener.wpc == screener_wpc)
        )
        screener = result.scalar_one_or_none()
        if screener:
            return ScreenerResponse.from_orm(screener)
        return None

    @staticmethod
    async def get_screener_with_instruments(db: AsyncSession, screener_wpc: str) -> Optional[ScreenerWithInstrumentsResponse]:
        # Retrieve the Screener instance
        screener_result = await db.execute(
            select(Screener).where(Screener.wpc == screener_wpc)
        )
        screener = screener_result.scalar_one_or_none()
        
        if not screener:
            return None
        
        # Retrieve associated ScreenerInstruments
        instruments_result = await db.execute(
            select(ScreenerInstrument).where(ScreenerInstrument.screener == screener_wpc)
        )
        instruments = instruments_result.scalars().all()

        return ScreenerWithInstrumentsResponse(
            screener=ScreenerResponse.from_orm(screener),
            instruments=[ScreenerInstrumentResponse.from_orm(instr) for instr in instruments]
        )
        
    
    @staticmethod
    async def get_stocks_custom_screener(db: AsyncSession, instruments: List[str], cols: List[str]):
        query = select(Stock).filter(Stock.isin.in_(instruments))
        result = await db.execute(query)
        stocks = result.scalars().all()
        
        basic_fields = ["wstockcode", "name", "isin", "bse_symbol", "nse_symbol"]
        cols = list(set(basic_fields + cols))
        
        return [StockResponse.from_orm(stock).dict(include=set(cols)) for stock in stocks]

    @staticmethod
    async def get_schemes_custom_screener(db: AsyncSession, instruments: List[str], cols: List[str]):
        query = select(Scheme).filter(Scheme.isin.in_(instruments))
        result = await db.execute(query)
        schemes = result.scalars().all()
        
        return [SchemeResponse.from_orm(scheme).dict(include=set(cols)) for scheme in schemes]

    @staticmethod
    async def get_screeners(db: AsyncSession, category: Optional[str] = None):
        categories = settings.DEFAULT_STOCK_SCREENERS
        
        if category:
            categories = [cat.strip() for cat in category.split(',')]

        query = select(Screener).filter(Screener.category.in_(categories), Screener.is_active == True)
        result = await db.execute(query)
        objs = result.scalars().all()

        categories_query = select(Screener.category, Screener.category_display_name) \
            .filter(Screener.category.in_(categories), Screener.is_active == True) \
            .order_by(Screener.category_order) \
            .distinct()
        categories_result = await db.execute(categories_query)
        categories = categories_result.all()

        screeners = []
        for cat, cat_dn in categories:
            f_objs = [obj for obj in objs if obj.category.lower() == cat.lower()]
            if not f_objs:
                continue

            cat_screeners = [ScreenerResponse.from_orm(obj).dict() for obj in f_objs]
            screener_details = {"id": cat, "name": cat_dn, "screeners": cat_screeners}
            screeners.append(screener_details)

        return screeners



#question

#q1 q2 q3 q4 q5 q6

#   q2value q4value
#  

# q1 q2 q3 q4 q5 q6 q7
# q1 
# q1
