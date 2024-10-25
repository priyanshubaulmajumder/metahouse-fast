from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, text
from datetime import date, datetime
import pytz
from decimal import Decimal
from app.models.stock_models import Stock, StockBSEHistPriceData, StockNSEHistPriceData
from app.schemas.stock_schemas import StockHistPriceDataBase
from app.core.config import settings
from app.utils.constants import ExchangeChoices, WHistoricalStockPricesField
from app.utils.constants import WCompanyMasterField
from app.services.modal_generic_service import ModalGenericService
from app.services.response_data_process_service import ResponseDataProcessService
from app.utils.helpers import get_decimal

class StockHistPriceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @classmethod
    async def execute_raw_query(cls, db: AsyncSession, query: str, exchange: str):
        if not query:
            return
        Modal = StockNSEHistPriceData if exchange == ExchangeChoices.NSE else StockBSEHistPriceData
        result = await db.execute(text(query))
        return result.fetchall()

    @staticmethod
    def get_raw_query_for_hprice(
            exchange: str, wstockcode: str, start_time: date = None, end_time: date = None,
            periodicity: str = 'd', fields: str = 'close'
    ):
        period = dict(d='day', w='week', m='month')
        periodicity = period[periodicity]
        modal = "stock_nse_hist_price_data" if exchange == ExchangeChoices.NSE else "stock_bse_hist_price_data"
        range_filter_str = ''
        if start_time:
            range_filter_str += f" and price_date >= '{start_time}'"
        if end_time:
            range_filter_str += f" and price_date <= '{end_time}'"
        return f"""
        select id, price_date, {fields} from (
            select id, price_date, {fields},
            row_number() OVER w AS rn 
            from {modal} 
            where wstockcode = :wstockcode {range_filter_str}
            window w AS (PARTITION BY date_trunc(:periodicity, price_date) ORDER BY price_date desc)
        ) as t 
        where rn = 1;
        """

    @staticmethod
    def get_raw_query_for_chart_hprice(
            exchange: str, wstockcode: str, start_time: date = None, end_time: date = None,
            periodicity: str = 'd'
    ):
        period = dict(d='day', w='week', m='month')
        periodicity = period[periodicity]
        modal = "stock_nse_hist_price_data" if exchange == ExchangeChoices.NSE else "stock_bse_hist_price_data"
        range_filter_str = ''
        if start_time:
            range_filter_str += f" and price_date >= '{start_time}'"
        if end_time:
            range_filter_str += f" and price_date <= '{end_time}'"
        return f"""
        SELECT distinct
            1 AS id,
            FIRST_VALUE(price_date) OVER w AS price_date,
            FIRST_VALUE(open) OVER w AS open,
            MAX(high) OVER w AS high,
            MIN(low) OVER w AS low,
            LAST_VALUE(close) OVER w AS close,
            SUM(volume) OVER w AS volume,
            SUM(value) OVER w AS value
        FROM
            {modal}
        WHERE
            wstockcode = :wstockcode {range_filter_str}
            WINDOW w AS (
                PARTITION BY DATE_TRUNC(:periodicity, price_date)
                ORDER BY price_date
                RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            )
        ORDER BY
            price_date
        """

    @classmethod
    async def get_hist_prices_for_wstockcode(
            cls, db: AsyncSession, exchange: str, wstockcode: str, start_date: date = None, end_date: date = None,
            periodicity: str = 'd', fields: str = 'close'
    ):
        if not (exchange and wstockcode and periodicity and fields):
            return
        query = cls.get_raw_query_for_hprice(
            exchange=exchange, wstockcode=wstockcode, start_time=start_date, end_time=end_date,
            periodicity=periodicity, fields=fields
        )
        params = {"wstockcode": wstockcode, "periodicity": periodicity}
        objs = await cls.execute_raw_query(db, query, exchange, params=params)
        return ResponseDataProcessService.stock_historical_prices(
            objs, fields.split(','), show_percentage_change=True
        ) or "Data not available"

 
    @staticmethod
    async def resync_historical_prices(db: AsyncSession, wstockcode: str, price_data: list, exchange: str):
        price_data = sorted(price_data, key=lambda x: x[WHistoricalStockPricesField.Date])
        price_dates = set([hp[WHistoricalStockPricesField.Date] for hp in price_data])
        Modal = StockBSEHistPriceData if exchange == ExchangeChoices.BSE else StockNSEHistPriceData
        
        query = select(Modal).filter(Modal.wstockcode == wstockcode)
        result = await db.execute(query)
        existing_prices = result.scalars().all()
        price_objs = {str(o.price_date): o for o in existing_prices}
        
        to_create_prices = price_dates.difference(price_objs.keys())
        objs_to_create, rows_to_update = [], []
        fields_to_update = [
            WHistoricalStockPricesField.Open, WHistoricalStockPricesField.Close, WHistoricalStockPricesField.High,
            WHistoricalStockPricesField.Low, WHistoricalStockPricesField.Value
        ]

        for i, hp in enumerate(price_data):
            diff, percentage_change = 0, 0
            prev_close = price_data[i-1][WHistoricalStockPricesField.Close] if i > 0 else None
            if prev_close:
                diff = get_decimal(hp[WHistoricalStockPricesField.Close] - prev_close)
                percentage_change = get_decimal((diff * 100) / prev_close)
            hp['diff'] = diff
            hp['percentage_change'] = percentage_change
            price_date = hp[WHistoricalStockPricesField.Date]
            
            if price_date in to_create_prices:
                obj = StockHistPriceDataBase(
                    wstockcode=wstockcode,
                    price_date=price_date,
                    open=hp[WHistoricalStockPricesField.Open],
                    close=hp[WHistoricalStockPricesField.Close],
                    low=hp[WHistoricalStockPricesField.Low],
                    high=hp[WHistoricalStockPricesField.High],
                    volume=hp[WHistoricalStockPricesField.Volume],
                    value=hp[WHistoricalStockPricesField.Value],
                    diff=diff,
                    percentage_change=percentage_change
                )
                objs_to_create.append(obj)
            else:
                data = {f: hp[f] for f in fields_to_update}
                data['diff'] = diff
                data['percentage_change'] = percentage_change
                data['price_date'] = price_date
                rows_to_update.append(data)

        await ModalGenericService.safe_bulk_create(db, Modal, objs_to_create)
        await ModalGenericService.optimized_update(
            db, Modal, {'price_date': 'price_date'}, ['price_date'], rows_to_update, 
            and_(Modal.wstockcode == wstockcode)
        )

    @classmethod
    async def get_max_starting_price_date_for_wstockcodes(
            cls, db: AsyncSession, exchange: str, wstockcodes: list, start_date: date = None, ignore_missing_stocks=False
    ):
        if not (exchange and wstockcodes):
            return None

        Modal = StockBSEHistPriceData if exchange == ExchangeChoices.BSE else StockNSEHistPriceData
        query = select(func.max(Modal.price_date).label('max_date'), func.count(Modal.wstockcode).label('count'))
        query = query.filter(Modal.wstockcode.in_(wstockcodes))
        
        if start_date:
            query = query.filter(Modal.price_date >= start_date)

        result = await db.execute(query)
        result = result.first()
        
        if result and (ignore_missing_stocks or len(wstockcodes) == result.count):
            return result.max_date
        return None

    @classmethod
    async def get_hist_prices_for_wstockcode(
            cls, db: AsyncSession, exchange: str, wstockcode: str, start_date: date = None, end_date: date = None,
            periodicity: str = 'd', fields: str = 'close'
    ):
        if not (exchange and wstockcode and periodicity and fields):
            return None

        Modal = StockBSEHistPriceData if exchange == ExchangeChoices.BSE else StockNSEHistPriceData
        query = select(Modal)
        query = query.filter(Modal.wstockcode == wstockcode)

        if start_date:
            query = query.filter(Modal.price_date >= start_date)
        if end_date:
            query = query.filter(Modal.price_date <= end_date)

        query = query.order_by(Modal.price_date)

        result = await db.execute(query)
        results = result.scalars().all()

        return ResponseDataProcessService.stock_historical_prices(
            results, fields.split(','), show_percentage_change=True
        ) or "Data not available"