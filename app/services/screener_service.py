from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.models.screener_models import Screener, ScreenerInstrument
from app.models.stock_models import Stock
from app.models.scheme_models import Scheme
from app.schemas.screener_schemas import ScreenerResponse, ScreenerInstrumentResponse
from app.schemas.stock_schemas import StockResponse
from app.schemas.scheme_schemas import SchemeSerializer as SchemeResponse
from typing import List, Optional
from app.core.config import settings
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
    async def get_screener(db: AsyncSession):
        # Implement your screener logic here
        return {"message": "Screener service"}
    """
    @staticmethod
    async def get_screeners(db: AsyncSession, category: Optional[str] = None):
        categories = settings.DEFAULT_STOCK_SCREENERS
        instrument_type_cache_key = f"screeners:stocks"
        
        if category:
            categories = [cat.strip() for cat in category.split(',')]
            instrument_type_cache_key = None

        if instrument_type_cache_key:
            cached_screeners = await cache.get(instrument_type_cache_key)
            if cached_screeners:
                return cached_screeners

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
            cache_key = f"screeners:{cat}"
            cached_screener = await cache.get(cache_key)
            if cached_screener:
                screeners.append(cached_screener)
                continue

            f_objs = [obj for obj in objs if obj.category.lower() == cat.lower()]
            if not f_objs:
                continue

            cat_screeners = [ScreenerResponse.from_orm(obj).dict() for obj in f_objs]
            screener_details = {"id": cat, "name": cat_dn, "screeners": cat_screeners}
            await cache.set(cache_key, screener_details, timeout=24 * 60 * 60)
            screeners.append(screener_details)

        if instrument_type_cache_key:
            await cache.set(instrument_type_cache_key, screeners, timeout=24 * 60 * 60)

        return screeners
    """
        
        
    
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


