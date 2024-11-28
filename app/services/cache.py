import datetime
import pytz
from app.utils.constants import NavTypeChoices, WShareHoldingEntity
#from app.constants.scheme_constants import MainCategoryChoices
from app.cache.redis_cache import get_cache_value, set_cache_value, delete_cache_key

class CacheKeysService:
    @staticmethod
    async def get_cache_value(key: str):
        return await get_cache_value(key)

    @staticmethod
    async def set_cache_value(key: str, value: str, expire: int = None):
        await set_cache_value(key, value, expire)

    @staticmethod
    async def delete_cache_key(key: str):
        await delete_cache_key(key)

    @staticmethod
    def get_stock_futures_market_live_news_cache_key(record_count: int = 50):
        if not record_count:
            return
        return f"1949_{record_count}_stock_futures_market_live_news"

    @staticmethod
    def get_company_specific_news_cache_key(cmots_id: str):
        if not cmots_id:
            return
        return f"1987_{cmots_id}_company_specific_news"

    @staticmethod
    def get_latest_hist_nav_updated_cache_key(wschemecode: str):
        if not wschemecode:
            return
        return f"6091_{wschemecode}_latest_hist_nav_updated"

    @staticmethod
    def get_hist_nav_last_processed_pointer_cache_key(service_name: str):
        if not service_name:
            return
        return f"9106_{service_name}_hist_nav_last_processed_pointer"

    @staticmethod
    def get_nfo_using_isin_cache_key(isin: str):
        if not isin:
            return
        return f"4910_{isin}_nfo_using_isin"

    @staticmethod
    def scheme_hnav_wpcs_cache_key():
        return f"scheme_hnav_wpc_2367"

    @staticmethod
    def schemes_third_party_id_to_wpc_mapping_cache_key():
        return f"schemes_third_party_id_to_wpc_mapping"

    @staticmethod
    def schemes_third_party_id_to_isin_mapping_cache_key():
        return f"schemes_third_party_id_to_isin_mapping"

    @staticmethod
    def parent_child_scheme_mapping_cache_key():
        return f"parent_child_scheme_mapping"

    @staticmethod
    def get_active_schemes_categories_cache_key(fund_type):
        return f"active_schemes_categories_{fund_type}"

    @staticmethod
    def get_active_schemes_wpcs_cache_key():
        return f"active_schemes_wpcs"

    @staticmethod
    def get_hist_nav_data_for_n_years_with_sip_day_cache_key(
            wpc, n_years, sip_day, include_right_end_edge_case=True, include_left_end_edge_case=True, nav_date_gte=None,
            show_percentage_change=False
    ):
        if not (wpc and n_years and sip_day):
            return
        if nav_date_gte:
            nav_date_gte = str(nav_date_gte)
        if show_percentage_change:
            return f"get_hnd_for_n_years_with_sip_day_{wpc}_{n_years}_{sip_day}_{include_left_end_edge_case}_{include_right_end_edge_case}_{nav_date_gte}_{show_percentage_change}_5540"
        return f"get_hnd_for_n_years_with_sip_day_{wpc}_{n_years}_{sip_day}_{include_left_end_edge_case}_{include_right_end_edge_case}_{nav_date_gte}_5540"

    @staticmethod
    def get_max_starting_nav_date_for_wpcs_cache_key(
            wpcs: list, start_date: datetime.date = None, ignore_missing_schemes=False
    ):
        if not wpcs:
            return
        return f"get_max_starting_nav_date_for_{str(start_date)}_{ignore_missing_schemes}_wpcs_{wpcs}_4398"

    @staticmethod
    def get_max_starting_price_date_for_wstockcodes_cache_key(
            exchange: str, wstockcodes: list, start_date: datetime.date = None, ignore_missing_stocks=False
    ):
        if not wstockcodes:
            return
        return f"get_max_starting_price_date_for_{exchange}_{str(start_date)}_{ignore_missing_stocks}_wstockcodes_{wstockcodes}_4398"

    @staticmethod
    def get_hist_prices_for_wstockcode_cache_key(
            exchange: str, wstockcode: str, start_date: datetime.date = None, end_date: datetime.date = None,
            periodicity: str = 'd', fields: str = 'close'
    ):
        if not (exchange and wstockcode and start_date and fields):
            return
        return f"get_hist_prices_for_{exchange}_wstockcode_{wstockcode}_{str(start_date)}_{str(end_date)}_{periodicity}_{fields}_6621"

    @staticmethod
    def get_stock_pre_session_live_news_cache_key(record_count: int = 50):
        if not record_count:
            return
        return f"stock_pre_session_live_news_{record_count}"

    @staticmethod
    def get_stock_mid_session_live_news_cache_key(record_count: int = 50):
        if not record_count:
            return
        return f"stock_mid_session_live_news_{record_count}"

    @staticmethod
    def get_stock_end_session_live_news_cache_key(record_count: int = 50):
        if not record_count:
            return
        return f"stock_end_session_live_news_{record_count}"

    @staticmethod
    def get_stock_economy_live_news_cache_key(record_count: int = 50):
        if not record_count:
            return
        return f"stock_economy_live_news_{record_count}"

    @staticmethod
    def get_stock_market_beat_live_news_cache_key(record_count: int = 50):
        if not record_count:
            return
        return f"stock_market_beat_live_news_{record_count}"

    @staticmethod
    def get_stock_hot_pursuit_live_news_cache_key(record_count: int = 50):
        if not record_count:
            return
        return f"stock_hot_pursuit_live_news_{record_count}"

    @staticmethod
    def get_stock_stock_alert_live_news_cache_key(record_count: int = 50):
        if not record_count:
            return
        return f"stock_stock_alert_live_news_{record_count}"

    @staticmethod
    def get_stock_specific_news_cache_key(news_id: str):
        if not news_id:
            return
        return f"stock_specific_news_{news_id}"