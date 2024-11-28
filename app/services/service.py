from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.scheme import SchemeHistNavData
from app.cache.redis_cache import get_cache_value, set_cache_value
from app.utils.futils import get_float, xirr
from utils.constants import NavTypeChoices, WHistoricalNAVField
from sqlalchemy import text
from dateutil.relativedelta import relativedelta
from fastapi import Depends
from app.db.session import get_db
from app.exceptions import WealthyValidationError
from app.utils.concurrent import execute_functions_concurrently
import logging
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("app")

class ReturnsCalculator:
    def __init__(self, data: Dict[str, Any]):
        self.wpc = data['wpc']
        self.amount = data['amount']
        self.n_years = data['n_years']
        self.investment_type = data['investment_type']
        self.sip_day = data['sip_day']  

    async def calculate_returns(self, db: AsyncSession) -> Dict[str, Any]:
        if self.investment_type == "Onetime":
            return await self.calculate_returns_for_onetime(db)
        elif self.investment_type == "Sip":
            return await self.calculate_returns_for_sip(db)
        return dict(
            invested_value=None, current_value=None, xirr=None, xirr_percentage=None,
            absolute_returns=None, absolute_returns_percentage=None, returns_details=None
        )

    async def calculate_returns_for_onetime(self, db: AsyncSession) -> Dict[str, Any]:
        returns_data = dict(
            invested_value=None, current_value=None, xirr=None, xirr_percentage=None,
            absolute_returns=None, absolute_returns_percentage=None, returns_details=[]
        )
        now = datetime.datetime.now().date()
        params = dict(wpc=self.wpc, n_years=self.n_years, sip_day=min(now.day, 28))
        nav_data = await self.get_hist_nav_data_for_n_years_with_sip_day(db, **params)
        current_nav_details = await self.get_current_nav_details(db)
        n_years_back_nav_details = await self.get_n_years_back_nav_details(db)
        
        current_nav = current_nav_details.adj_nav or 0
        if not current_nav:
            return returns_data
        n_years_back_nav = n_years_back_nav_details.adj_nav or 0
        if not n_years_back_nav:
            return returns_data
        units = get_float(self.amount / n_years_back_nav)
        for nd in nav_data:
            nd.units = units
            nd.invested_value = self.amount
            nd.current_value = get_float(units * nd.adj_nav, decimal_places=2)
        current_nav_date = str(current_nav_details.nav_date)
        dates = [n_years_back_nav_details.nav_date, current_nav_date]
        current_nav = get_float(current_nav)
        if nav_data[-1].nav_date != current_nav_date:
            current_nav_details.nav_date = current_nav_date
            current_nav_details.nav = current_nav_details.nav or 0
            current_nav_details.nav = get_float(current_nav_details.nav)
            current_nav_details.adj_nav = current_nav
            current_nav_details.units = units
            current_nav_details.invested_value = self.amount
            current_nav_details.current_value = get_float(units * current_nav, decimal_places=2)
            nav_data.append(current_nav_details)
        current_value = nav_data[-1].current_value
        cashflows = [-self.amount, current_value]
        xirr_value = get_float(xirr(dates, cashflows), decimal_places=7)
        diff = get_float(current_value - self.amount)
        returns_data['invested_value'] = self.amount
        returns_data['current_value'] = current_value
        returns_data['xirr'] = xirr_value
        returns_data['diff'] = diff
        returns_data['nav_data'] = nav_data
        return returns_data

    async def get_current_nav_details(self, db: AsyncSession) -> SchemeHistNavData:
        cache_key = f"current_nav_details_{self.wpc}"
        cached_value = await get_cache_value(cache_key)
        if cached_value:
            return SchemeHistNavData(**cached_value)
        result = await db.execute(select(SchemeHistNavData).filter(SchemeHistNavData.wpc == self.wpc).order_by(SchemeHistNavData.nav_date.desc()).limit(1))
        current_nav_details = result.scalars().first()
        await set_cache_value(cache_key, current_nav_details, expire=3600)
        return current_nav_details

    async def get_n_years_back_nav_details(self, db: AsyncSession) -> SchemeHistNavData:
        cache_key = f"n_years_back_nav_details_{self.wpc}_{self.n_years}"
        cached_value = await get_cache_value(cache_key)
        if cached_value:
            return SchemeHistNavData(**cached_value)
        n_years_back_date = datetime.date.today() - datetime.timedelta(days=self.n_years * 365)
        result = await db.execute(select(SchemeHistNavData).filter(SchemeHistNavData.wpc == self.wpc, SchemeHistNavData.nav_date <= n_years_back_date).order_by(SchemeHistNavData.nav_date.desc()).limit(1))
        n_years_back_nav_details = result.scalars().first()
        await set_cache_value(cache_key, n_years_back_nav_details, expire=3600)
        return n_years_back_nav_details

    async def get_hist_nav_data_for_n_years_with_sip_day(self, db: AsyncSession, wpc: str, n_years: int, sip_day: int) -> List[SchemeHistNavData]:
        cache_key = f"nav_data_{wpc}_{n_years}_{sip_day}"
        cached_value = await get_cache_value(cache_key)
        if cached_value:
            return [SchemeHistNavData(**nav) for nav in cached_value]
        n_years_back_date = datetime.date.today() - datetime.timedelta(days=n_years * 365)
        result = await db.execute(select(SchemeHistNavData).filter(SchemeHistNavData.wpc == wpc, SchemeHistNavData.nav_date >= n_years_back_date).order_by(SchemeHistNavData.nav_date))
        nav_data = result.scalars().all()
        await set_cache_value(cache_key, [nav.__dict__ for nav in nav_data], expire=3600)
        return nav_data
    
    


class SchemeHistNavService:
    Modal = SchemeHistNavData

    @classmethod
   # @from_cache(cache_func=CacheKeysService.scheme_hist_nav_data_cache_key, timeout=60 * 60)
    async def get_hist_nav_data(cls, db:AsyncSession , wpc, nav_type):
        nav_data = {}
        if not wpc:
            return nav_data
        vl = ['nav_date', 'nav']
        if nav_type == NavTypeChoices.AdjNav:
            vl = ['nav_date', 'adj_nav']
        result = await db.execute(select(cls.Modal).filter_by(wpc=wpc).order_by(cls.Modal.nav_date).with_only_columns(vl))
        nav_data = {str(nd[0]): nd[1] for nd in result.all()}
        return nav_data

    @classmethod
   # @from_cache(cache_func=CacheKeysService.scheme_hist_nav_data_for_n_years_cache_key, timeout=3 * 60 * 60)
    async def get_hist_nav_data_for_n_years(cls, db: AsyncSession, wpc: str, years: int, step: int = 1, as_list: bool = False, nav_type: str = 'Nav') -> Any:
        nav_data = {}
        if not (wpc and years):
            return nav_data
        now = datetime.now().date()
        vl = ['nav_date', 'nav']
        if nav_type == NavTypeChoices.AdjNav:
            vl = ['nav_date', 'adj_nav']
        result = await db.execute(select(cls.Modal).filter(cls.Modal.wpc == wpc, cls.Modal.nav_date >= now - relativedelta(years=years)).order_by(cls.Modal.nav_date).with_only_columns(vl))
        if as_list:
            nav_data = [[str(nd[0]), get_float(nd[1])] for nd in result.all()[::step]]
        else:
            nav_data = {str(nd[0]): get_float(nd[1]) for nd in result.all()[::step]}
        return nav_data

    @classmethod
    async def get_as_on_hist_nav_data(cls, db: AsyncSession, wpc: str, as_on: datetime, approx: bool = True) -> Dict[str, Any]:
        nav_data = dict(nav_date=None, nav=None, adj_nav=None)
        if not (wpc and as_on):
            return nav_data
        if not approx:
            q = cls.Modal.wpc == wpc, cls.Modal.nav_date == as_on
        else:
            q = cls.Modal.wpc == wpc, cls.Modal.nav_date <= as_on
        result = await db.execute(select(cls.Modal).filter(*q).order_by(cls.Modal.nav_date.desc()).limit(1))
        hist_nav_obj = result.scalar_one_or_none()
        if not hist_nav_obj:
            return nav_data
        if hist_nav_obj.nav_date == as_on or approx:
            return dict(
                nav_date=hist_nav_obj.nav_date, nav=hist_nav_obj.nav, adj_nav=hist_nav_obj.adj_nav
            )
        return nav_data

    @classmethod
   # @from_cache(cache_func=CacheKeysService.get_hist_nav_data_for_n_years_with_sip_day_cache_key, timeout=6 * 60 * 60)
    async def get_hist_nav_data_for_n_years_with_sip_day(
            cls, db: AsyncSession, wpc: str, n_years: int, sip_day: int, include_left_end_edge_case: bool = True, include_right_end_edge_case: bool = True,
            nav_date_gte: Optional[datetime] = None, show_percentage_change: bool = False
    ) -> List[Dict[str, Any]]:
        if not (wpc and n_years and sip_day):
            return []
        raw_query = cls.get_raw_query_for_n_years_with_sip_day_hist_nav_data(
            wpc=wpc, n_years=n_years, sip_day=sip_day,
            include_left_end_edge_case=include_left_end_edge_case,
            include_right_end_edge_case=include_right_end_edge_case,
            nav_date_gte=nav_date_gte
        )
        result = await db.execute(text(raw_query))
        nav_objs = result.fetchall()
        if not show_percentage_change:
            return [
                dict(nav_date=str(no.nav_date), nav=get_float(no.nav), adj_nav=get_float(no.adj_nav)) for no in nav_objs
            ]
        results, first_adj_nav = [], None
        for no in nav_objs:
            first_adj_nav = no.adj_nav if first_adj_nav is None else first_adj_nav
            percentage_change = get_float(((no.adj_nav - first_adj_nav) * 100) / first_adj_nav, decimal_places=2)
            results.append(dict(
                nav_date=str(no.nav_date), nav=get_float(no.nav), adj_nav=get_float(no.adj_nav),
                percentage_change=percentage_change
            ))
        return results


    @staticmethod
    def get_raw_query_for_n_years_with_sip_day_hist_nav_data(
            wpc: str, n_years: int, sip_day: int, include_left_end_edge_case: bool = True, include_right_end_edge_case: bool = True, nav_date_gte: Optional[datetime] = None
    ) -> str:
        if not (n_years and sip_day):
            return ""
        if nav_date_gte:
            nav_date_gte = max(datetime.now().date() - relativedelta(years=n_years), nav_date_gte)
        else:
            nav_date_gte = datetime.now().date() - relativedelta(years=n_years)
        if nav_date_gte.day > sip_day:
            nav_date_gte = nav_date_gte + relativedelta(months=1)
            nav_date_gte = nav_date_gte + relativedelta(day=1)
        query = f"SELECT id, wpc, nav, nav_date, adj_nav " \
               f"FROM (SELECT id, wpc, nav_date, nav, adj_nav, " \
               f"lag(nav_date, 1, nav_date) over w as lag_date, " \
               f"lead(nav_date, 1, nav_date) over w as lead_date, " \
               f"TO_DATE(CONCAT(EXTRACT(YEAR FROM nav_date), '-', EXTRACT(MONTH FROM nav_date), '-', '{sip_day}'), 'YYYY-MM-DD') as required_date " \
               f"from SchemeHistNavData WHERE wpc = '{wpc}' and nav_date >= '{nav_date_gte}' " \
               f"window w as (PARTITION BY TO_DATE(CONCAT(EXTRACT(YEAR FROM nav_date), '-', EXTRACT(MONTH FROM nav_date), '-', '01'), 'YYYY-MM-DD') ORDER BY nav_date asc)) as t " \
               f"where (lag_date < required_date and required_date <= nav_date)"
        if include_left_end_edge_case:
            query += " or (lag_date = nav_date and required_date <= nav_date)"
        if include_right_end_edge_case:
            query += " or (nav_date = lead_date and (required_date > nav_date and required_date < CURRENT_DATE))"
        return query + ";"

    @staticmethod
    def get_raw_query_for_multiple_ids_for_as_on_date(wpcs: List[str], as_on: datetime, gt: bool = False) -> str:
        if not (wpcs and as_on):
            raise ValueError("The list of WPCs and the as_on date cannot be empty.")
        fields = ['wpc', 'nav_date', 'nav', 'adj_nav']
        fields = ", ".join(fields)
        wpcs_str = ", ".join(f"'{wpc}'" for wpc in wpcs)
        modal = "SchemeHistNavData"
        range_filter_str = f"and nav_date <= '{str(as_on)}'"
        order_by = 'desc'
        if gt:
            range_filter_str = f"and nav_date > '{str(as_on)}'"
            order_by = 'asc'
        return f"select id, {fields} from (select id, {fields}, " \
               f"row_number() OVER w AS rn from public.{modal} where wpc in ({wpcs_str}) {range_filter_str} " \
               f"window w AS (PARTITION BY wpc ORDER BY nav_date {order_by})) as t where rn = 1 order by wpc;"
               


    @staticmethod
    def get_raw_query_for_max_starting_nav_date_for_wpcs(wpcs: List[str], start_date: Optional[datetime.date] = None) -> str:
        if not wpcs:
            raise ValueError("The list of WPCs cannot be empty.")
        modal = "SchemeHistNavData"
        wpcs_str = ", ".join(f"'{wpc}'" for wpc in wpcs)
        start_date_str = f" and nav_date >= '{start_date}'" if start_date else ""
        return f"SELECT 1 as id, max(nav_date) as max_date, count(nav_date) as counts FROM (" \
               f"SELECT nav_date, row_number() over w as rn FROM " \
               f"public.{modal} WHERE " \
               f"wpc in ({wpcs_str}) {start_date_str}" \
               f"window w as (PARTITION BY wpc ORDER BY nav_date asc)) as t WHERE " \
               f"t.rn = 1;"
               

    @staticmethod
    def get_raw_query_for_hist_navs(wpc: str, start_date: Optional[datetime.date], end_date: Optional[datetime.date], periodicity: str) -> str:
        modal = "SchemeHistNavData"
        period = dict(d='day', w='week', m='month')
        periodicity = period[periodicity]
        range_filter_str = ''
        if start_date:
            range_filter_str += f" and nav_date >= '{start_date}'"
        if end_date:
            range_filter_str += f" and nav_date <= '{end_date}'"
        return f"select id, nav_date, nav, adj_nav from (select id, nav_date, nav, adj_nav, " \
               f"row_number() OVER w AS rn from public.{modal} where wpc = '{wpc}'{range_filter_str} " \
               f"window w AS (PARTITION BY date_trunc('{periodicity}', nav_date) ORDER BY nav_date desc)) as t " \
               f"where rn = 1;"

    @staticmethod
    def get_raw_query_for_hist_navs(wpc, start_date, end_date, periodicity):
        modal = "SchemeHistNavData"
        period = dict(d='day', w='week', m='month')
        periodicity = period[periodicity]
        range_filter_str = ''
        if start_date:
            range_filter_str += f" and nav_date >= '{start_date}'"
        if end_date:
            range_filter_str += f" and nav_date <= '{end_date}'"
        return f"select id, nav_date, nav, adj_nav from (select id, nav_date, nav, adj_nav, " \
               f"row_number() OVER w AS rn from public.{modal} where wpc = '{wpc}'{range_filter_str} " \
               f"window w AS (PARTITION BY date_trunc('{periodicity}', nav_date) ORDER BY nav_date desc)) as t " \
               f"where rn = 1;"

    @classmethod
   # @from_cache(cache_func=CacheKeysService.get_max_starting_nav_date_for_wpcs_cache_key, timeout=24 * 60 * 60)
    async def get_max_starting_nav_date_for_wpcs(
            cls, db: AsyncSession, wpcs: List[str], start_date: Optional[datetime.date] = None, ignore_missing_schemes: bool = False
    ) -> Optional[datetime.date]:
        if not wpcs:
            return None
        raw_query = cls.get_raw_query_for_max_starting_nav_date_for_wpcs(wpcs=wpcs, start_date=start_date)
        result = await db.execute(text(raw_query))
        objs = result.fetchall()
        if not objs:
            return None
        max_date = objs[0].max_date
        if not ignore_missing_schemes and len(wpcs) != objs[0].counts:
            return None
        return max_date

    @classmethod
    async def execute_raw_query(cls, db: AsyncSession, query: str) -> Any:
        if not query:
            return None
        result = await db.execute(text(query))
        return result.fetchall()
    
    @staticmethod
    def process_hist_nav_data_for_multiple_ids(req_keys, nav_data, as_on, col, mapping, approx=True):
        final_data = []
        if not (req_keys and nav_data and as_on and col and mapping):
            return final_data
        nav_data_dict = {nd.wpc: nd for nd in nav_data}
        for req_key in req_keys:
            wpc = mapping[req_key]
            base_nd = dict(id_type=col, id_value=req_key, nav_date=None, nav=None, adj_nav=None)
            nd = nav_data_dict.get(wpc)
            if nd and (approx or nd.nav_date == as_on):
                base_nd.update(dict(nav_date=str(nd.nav_date), nav=nd.nav, adj_nav=nd.adj_nav))
            final_data.append(base_nd)
        return final_data

    @staticmethod
    def make_scheme_hnav_obj(wpc, data):
        if not (wpc and data and isinstance(data, dict)):
            return
        return SchemeHistNavData(
            wpc=wpc, nav_date=data[WHistoricalNAVField.NAVDate],
            nav=data[WHistoricalNAVField.NAV], adj_nav=data[WHistoricalNAVField.AdjNAV],
            diff=data['diff'], percentage_change=data['percentage_change']
        )

    @classmethod
    def populate_hist_nav_for_nfo(cls, scheme_obj):
        if not scheme_obj:
            return
        temp_date = scheme_obj.launch_date
        close_date = scheme_obj.close_date
        if not (temp_date and close_date):
            return
        wpc = scheme_obj.wpc
        nav = scheme_obj.nav_at_launch
        hist_nav_objs = []
        while temp_date <= close_date:
            data = dict(nav=nav, adj_nav=nav, nav_date=temp_date, diff=0, percentage_change=0)
            hist_nav_obj = cls.make_scheme_hnav_obj(wpc, data)
            if hist_nav_obj:
                hist_nav_objs.append(hist_nav_obj)
            temp_date = temp_date + datetime.timedelta(days=1)
        offset, limit = 0, 100
        for offset in range(offset, len(hist_nav_objs), limit):
            ModalGenericService.safe_bulk_create(Modal=SchemeHistNavData, objs=hist_nav_objs[offset: offset + limit])

    @classmethod
   # @from_cache(cache_func=CacheKeysService.get_hist_navs_for_wpc_cache_key, timeout_at=datetime.time(hour=11, minute=0, second=0, tzinfo=pytz.timezone(settings.INDIAN_TZ)))
    async def get_hist_navs_for_wpc(
            cls, db: AsyncSession, wpc: str, start_date: datetime.date = None, end_date: datetime.date = None, periodicity: str = 'd'
    ):
        if not (wpc and periodicity):
            return
        query = cls.get_raw_query_for_hist_navs(wpc=wpc, start_date=start_date, end_date=end_date, periodicity=periodicity)
        objs = await cls.execute_raw_query(db, query=query)
        results = []
        first_adj_nav = None
        for o in objs:
            first_adj_nav = o.adj_nav if first_adj_nav is None else first_adj_nav
            percentage_change = get_float(((o.adj_nav - first_adj_nav) * 100) / first_adj_nav, decimal_places=2)
            results.append([str(o.nav_date), str(o.nav), str(o.adj_nav), percentage_change])
        return results or "Data not available"


    @classmethod
    async def get_hist_navs_for_wpcs(cls, db: AsyncSession, wpcs: list, start_date: datetime.date):
        if not (wpcs and start_date):
            return
        end_date = datetime.now().date()
        delta = (end_date - start_date).days
        periodicity = 'd'
        if delta > 366:
            periodicity = 'w'
        kl = []
        for wpc in wpcs:
            params_data = dict(wpc=wpc, start_date=start_date, end_date=end_date, periodicity=periodicity)
            kl.append(dict(**params_data, cache_func_kwargs=params_data))
        resp = await execute_functions_concurrently(
            functions_list=[cls.get_hist_navs_for_wpc] * len(kl), kwargs_list=kl,
            workers_count=len(kl), raise_exception=False
        )
        results = {}
        for r in resp:
            results.update(r)
        if not results:
            raise WealthyValidationError("Invalid request")
        final_result = {}
        for i, wpc in enumerate(wpcs):
            final_result[wpc] = results[i]
        return final_result

    
    
class ModalGenericService:

    @staticmethod
    async def safe_bulk_create(db: AsyncSession, Modal, objs: list, batch_size=100) -> None:
        if not (objs and isinstance(objs, list)):
            return
        if not isinstance(objs[0], Modal):
            return
        try:
            for i in range(0, len(objs), batch_size):
                batch = objs[i:i + batch_size]
                db.add_all(batch)
                await db.commit()
        except SQLAlchemyError as e:
            logger.error(f"Failed to bulk create for model {Modal}. {e}")
            for obj in objs:
                try:
                    db.add(obj)
                    await db.commit()
                except SQLAlchemyError as e:
                    logger.error(f"Failed to save object {obj}. {e}")
                    await db.rollback()