from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, text
from app.models.scheme import Scheme #SchemeHolding
from app.crud.scheme import SchemeCreate, SchemeUpdate, SchemeHoldingCreate
from typing import List, Optional, Any
from datetime import date, datetime
from decimal import Decimal
from collections import defaultdict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.services.cache import CacheKeysService
from app.models.scheme import WSchemeCodeWPCMapping, ISINWPCMapping, SchemeCodeWPCMapping, TPSLSchemeCodeWPCMapping,WPCToTWPCMapping
from app.cache.redis_cache import get_cache_value, set_cache_value
class SchemeService:
    @staticmethod
    def get_scheme(db: Session, wschemecode: str) -> Optional[Scheme]:
        return db.query(Scheme).filter(Scheme.wschemecode == wschemecode).first()

    @staticmethod
    def get_scheme_by_wpc(db: Session, wpc: str) -> Optional[Scheme]:
        return db.query(Scheme).filter(Scheme.wpc == wpc).first()

    @staticmethod
    def get_schemes(db: Session, skip: int = 0, limit: int = 100) -> List[Scheme]:
        return db.query(Scheme).offset(skip).limit(limit).all()

    @staticmethod
    def create_scheme(db: Session, scheme: SchemeCreate) -> Scheme:
        db_scheme = Scheme(**scheme.dict())
        db.add(db_scheme)
        db.commit()
        db.refresh(db_scheme)
        return db_scheme

    @staticmethod
    def update_scheme(db: Session, wschemecode: str, scheme: SchemeUpdate) -> Optional[Scheme]:
        db_scheme = SchemeService.get_scheme(db, wschemecode)
        if db_scheme:
            for key, value in scheme.dict(exclude_unset=True).items():
                setattr(db_scheme, key, value)
            db.commit()
            db.refresh(db_scheme)
        return db_scheme

    @staticmethod
    def delete_scheme(db: Session, wschemecode: str) -> bool:
        db_scheme = SchemeService.get_scheme(db, wschemecode)
        if db_scheme:
            db.delete(db_scheme)
            db.commit()
            return True
        return False
#metahouse e nei eta
    # @staticmethod
    # def get_scheme_holdings(db: Session, wpc: str) -> List[SchemeHolding]:
    #     return db.query(SchemeHolding).filter(SchemeHolding.wpc == wpc).all()

    # @staticmethod
    # def create_scheme_holding(db: Session, holding: SchemeHoldingCreate) -> SchemeHolding:
    #     db_holding = SchemeHolding(**holding.dict())
    #     db.add(db_holding)
    #     db.commit()
    #     db.refresh(db_holding)
    #     return db_holding

    @staticmethod
    def get_schemes_by_category(db: Session, category: str) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.category == category).all()

    @staticmethod
    def get_schemes_by_amc(db: Session, amc: str) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.amc == amc).all()

    @staticmethod
    def get_schemes_by_fund_type(db: Session, fund_type: str) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.fund_type == fund_type).all()

    @staticmethod
    def get_schemes_by_risk_o_meter(db: Session, risk_o_meter_value: str) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.risk_o_meter_value == risk_o_meter_value).all()

    @staticmethod
    def get_tax_saver_schemes(db: Session) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.category.ilike('%elss%')).all()

    @staticmethod
    def get_schemes_by_aum_range(db: Session, min_aum: Decimal, max_aum: Decimal) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.aum.between(min_aum, max_aum)).all()

    @staticmethod
    def get_schemes_by_launch_date_range(db: Session, start_date: date, end_date: date) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.launch_date.between(start_date, end_date)).all()

    @staticmethod
    def get_schemes_by_benchmark(db: Session, benchmark: str) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.benchmark == benchmark).all()

    @staticmethod
    def get_schemes_by_fund_manager(db: Session, fund_manager: str) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.fund_manager.ilike(f'%{fund_manager}%')).all()

    @staticmethod
    def get_schemes_by_wealthy_select(db: Session, wealthy_select: bool) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.wealthy_select == wealthy_select).all()

    @staticmethod
    def get_schemes_by_w_rating_range(db: Session, min_rating: Decimal, max_rating: Decimal) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.w_rating.between(min_rating, max_rating)).all()

    @staticmethod
    def get_active_schemes(db: Session) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.deprecated_at.is_(None)).all()

    @staticmethod
    def get_deprecated_schemes(db: Session) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.deprecated_at.isnot(None)).all()

    @staticmethod
    def search_schemes(db: Session, query: str) -> List[Scheme]:
        return db.query(Scheme).filter(
            or_(
                Scheme.scheme_name.ilike(f'%{query}%'),
                Scheme.display_name.ilike(f'%{query}%'),
                Scheme.category.ilike(f'%{query}%'),
                Scheme.amc.ilike(f'%{query}%')
            )
        ).all()

    @staticmethod
    def get_schemes_with_high_ytm(db: Session, ytm_threshold: Decimal) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.yield_till_maturity >= ytm_threshold).all()

    @staticmethod
    def get_schemes_by_exit_load(db: Session, has_exit_load: bool) -> List[Scheme]:
        if has_exit_load:
            return db.query(Scheme).filter(Scheme.exit_load_percentage > 0).all()
        else:
            return db.query(Scheme).filter(or_(Scheme.exit_load_percentage == 0, Scheme.exit_load_percentage.is_(None))).all()

    @staticmethod
    def get_schemes_by_lock_in_period(db: Session, has_lock_in: bool) -> List[Scheme]:
        if has_lock_in:
            return db.query(Scheme).filter(Scheme.lock_in_time > 0).all()
        else:
            return db.query(Scheme).filter(or_(Scheme.lock_in_time == 0, Scheme.lock_in_time.is_(None))).all()

    @staticmethod
    def get_schemes_by_return_type(db: Session, return_type: str) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.return_type == return_type).all()

    @staticmethod
    def get_schemes_by_plan_type(db: Session, plan_type: str) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.plan_type == plan_type).all()

    @staticmethod
    def get_schemes_by_taxation_type(db: Session, taxation_type: str) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.taxation_type == taxation_type).all()

    @staticmethod
    def get_schemes_by_nav_range(db: Session, min_nav: Decimal, max_nav: Decimal) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.nav.between(min_nav, max_nav)).all()

    @staticmethod
    def get_schemes_by_latest_nav_date(db: Session, nav_date: date) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.nav_date == nav_date).all()

    @staticmethod
    def get_schemes_by_w_score_range(db: Session, min_score: Decimal, max_score: Decimal) -> List[Scheme]:
        return db.query(Scheme).filter(Scheme.w_score.between(min_score, max_score)).all()
    
    @staticmethod
    async def get_schemes_data(
        db: AsyncSession,
        cols: Optional[List[str]] = None,
        order_by: str = '-created_at',
        allow_deprecated: bool = False,
        allow_null_tpids: bool = False,
        flat: Optional[bool] = None,
        q: Optional[List[Any]] = None,
        values: bool = False
    ) -> Any:
        filters = []
        if q:
            filters.extend(q)
        if not allow_null_tpids:
            filters.append(Scheme.third_party_id.isnot(None))
        if not allow_deprecated:
            filters.append(Scheme.deprecated_at.is_(None))

        # Determine order direction
        descending = False
        if order_by.startswith('-'):
            descending = True
            order_column_name = order_by[1:]
        else:
            order_column_name = order_by

        # Get the column object from the Scheme model
        try:
            order_column = getattr(Scheme, order_column_name)
        except AttributeError:
            raise ValueError(f"Invalid order_by column: {order_column_name}")

        # Apply ordering
        if descending:
            order_clause = order_column.desc()
        else:
            order_clause = order_column.asc()

        # Build the base query
        if cols:
            # Ensure all specified columns exist in Scheme model
            try:
                selected_columns = [getattr(Scheme, col) for col in cols]
            except AttributeError as e:
                raise ValueError(f"Invalid column specified: {e}")
            query = select(*selected_columns).where(and_(*filters)).order_by(order_clause)
        else:
            query = select(Scheme).where(and_(*filters)).order_by(order_clause)

        # Execute the query
        result = await db.execute(query)

        if cols:
            if values or isinstance(cols, set):
                # Return list of dictionaries
                schemes = result.mappings().all()
                return schemes
            else:
                if flat is None:
                    flat = len(cols) == 1
                rows = result.all()
                if flat:
                    # Return flat list of values from the first column
                    return [row[0] for row in rows]
                else:
                    # Return list of tuples
                    return rows
        else:
            schemes = result.scalars().all()
            if values:
                # Return list of dictionaries
                return [Scheme(**scheme.__dict__) for scheme in schemes]
            else:
                # Return ORM objects
                return schemes
            

'''
class SchemeUniqueIDsCacheService:

    @staticmethod
    async def get_wschemecode_wpc_mapping(db: AsyncSession, refresh=False):
        cache_key = CacheKeysService.get_wschemecode_wpc_mapping_cache_key()
        if not refresh:
            mapping = await get_cache_value(cache_key)
            if mapping:
                return mapping
        result = await db.execute(select(WSchemeCodeWPCMapping).filter_by(hidden=False))
        objs = result.scalars().all()
        mapping = defaultdict(list)
        for o in objs:
            mapping[o.wschemecode].append(o.wpc)
        await set_cache_value(cache_key, mapping, expire=24 * 60 * 60)
        return mapping

    @staticmethod
    async def get_isin_wpc_mapping(db: AsyncSession, refresh=False):
        cache_key = CacheKeysService.get_isin_wpc_mapping_cache_key()
        if not refresh:
            mapping = await get_cache_value(cache_key)
            if mapping:
                return mapping
        result = await db.execute(select(ISINWPCMapping).filter_by(hidden=False))
        objs = result.scalars().all()
        mapping = defaultdict(list)
        for o in objs:
            mapping[o.isin].append(o.wpc)
        await set_cache_value(cache_key, mapping, expire=24 * 60 * 60)
        return mapping

    @staticmethod
    async def get_scheme_code_wpc_mapping(db: AsyncSession, refresh=False):
        cache_key = CacheKeysService.get_scheme_code_wpc_mapping_cache_key()
        if not refresh:
            mapping = await get_cache_value(cache_key)
            if mapping:
                return mapping
        result = await db.execute(select(SchemeCodeWPCMapping).filter_by(hidden=False))
        objs = result.scalars().all()
        mapping = defaultdict(list)
        for o in objs:
            mapping[o.scheme_code].append(o.wpc)
        await set_cache_value(cache_key, mapping, expire=24 * 60 * 60)
        return mapping

    @staticmethod
    async def get_wpc_to_target_wpc_mapping(db: AsyncSession, refresh=False):
        cache_key = CacheKeysService.get_wpc_to_twpc_mapping_cache_key()
        if not refresh:
            mapping = await get_cache_value(cache_key)
            if mapping:
                return mapping
        result = await db.execute(select(WPCToTWPCMapping).filter_by(hidden=False))
        objs = result.scalars().all()
        mapping = {o.wpc: o.target_wpc for o in objs}
        await set_cache_value(cache_key, mapping, expire=24 * 60 * 60)
        return mapping

    @staticmethod
    def get_scheme_code_combinations(scheme_code):
        if not scheme_code:
            return []
        scheme_codes = [scheme_code[:-1]]
        append_letters = ['G', 'R', 'D']
        for append_letter in append_letters:
            scheme_codes.append(f"{scheme_code}{append_letter}")
        return scheme_codes

    @staticmethod
    async def get_wschemecode_wpc_mapping_from_db(db: AsyncSession, wschemecodes):
        if not wschemecodes:
            return {}
        result = await db.execute(select(WSchemeCodeWPCMapping).filter(WSchemeCodeWPCMapping.wschemecode.in_(wschemecodes), WSchemeCodeWPCMapping.hidden == False).order_by(WSchemeCodeWPCMapping.created_at))
        objs = result.scalars().all()
        mapping = defaultdict(list)
        for o in objs:
            mapping[o.wschemecode].append(o.wpc)
        return mapping

    @staticmethod
    async def get_isin_wpc_mapping_from_db(db: AsyncSession, isins):
        if not isins:
            return {}
        result = await db.execute(select(ISINWPCMapping).filter(ISINWPCMapping.isin.in_(isins), ISINWPCMapping.hidden == False).order_by(ISINWPCMapping.created_at))
        objs = result.scalars().all()
        mapping = defaultdict(list)
        for o in objs:
            mapping[o.isin].append(o.wpc)
        return mapping

    @staticmethod
    async def get_scheme_code_wpc_mapping_from_db(db: AsyncSession, scheme_codes):
        if not scheme_codes:
            return {}
        result = await db.execute(select(SchemeCodeWPCMapping).filter(SchemeCodeWPCMapping.scheme_code.in_(scheme_codes), SchemeCodeWPCMapping.hidden == False).order_by(SchemeCodeWPCMapping.created_at))
        objs = result.scalars().all()
        mapping = defaultdict(list)
        for o in objs:
            mapping[o.scheme_code].append(o.wpc)
        return mapping

    @staticmethod
    async def get_tpsl_scheme_code_wpc_mapping_from_db(db: AsyncSession, tpsl_scheme_codes):
        if not tpsl_scheme_codes:
            return {}
        result = await db.execute(select(TPSLSchemeCodeWPCMapping).filter(TPSLSchemeCodeWPCMapping.tpsl_scheme_code.in_(tpsl_scheme_codes), TPSLSchemeCodeWPCMapping.hidden == False).order_by(TPSLSchemeCodeWPCMapping.created_at))
        objs = result.scalars().all()
        mapping = defaultdict(list)
        for o in objs:
            mapping[o.tpsl_scheme_code].append(o.wpc)
        return mapping

    @classmethod
    async def resolve_wpcs_from_wschemecodes(cls, db: AsyncSession, wschemecodes):
        resolved, resolved_new_wpcs, unresolved = {}, {}, []
        if not (wschemecodes and isinstance(wschemecodes, list)):
            return resolved, resolved_new_wpcs, unresolved
        mapping = await cls.get_wschemecode_wpc_mapping_from_db(db, wschemecodes)
        for wsc in wschemecodes:
            if mapping.get(wsc):
                wpc = mapping[wsc][0]
                resolved[wsc] = wpc
                if len(mapping[wsc]) > 1:
                    resolved_new_wpcs[wsc] = mapping[wsc][-1]
            else:
                unresolved.append(wsc)
        return resolved, resolved_new_wpcs, unresolved

    @classmethod
    async def resolve_wpcs_from_isins(cls, db: AsyncSession, isins):
        resolved, resolved_new_wpcs, unresolved = {}, {}, []
        if not (isins and isinstance(isins, list)):
            return resolved, resolved_new_wpcs, unresolved
        mapping = await cls.get_isin_wpc_mapping_from_db(db, isins)
        for isin in isins:
            if mapping.get(isin):
                wpc = mapping[isin][0]
                resolved[isin] = wpc
                if len(mapping[isin]) > 1:
                    resolved_new_wpcs[isin] = mapping[isin][-1]
            else:
                unresolved.append(isin)
        return resolved, resolved_new_wpcs, unresolved

    @classmethod
    async def resolve_wpcs_from_scheme_codes(cls, db: AsyncSession, scheme_codes):
        resolved, resolved_new_wpcs, unresolved = {}, {}, []
        if not (scheme_codes and isinstance(scheme_codes, list)):
            return resolved, resolved_new_wpcs, unresolved
        mapping = await cls.get_scheme_code_wpc_mapping_from_db(db, scheme_codes)
        for scheme_code in scheme_codes:
            if mapping.get(scheme_code):
                wpc = mapping[scheme_code][0]
                resolved[scheme_code] = wpc
                if len(mapping[scheme_code]) > 1:
                    resolved_new_wpcs[scheme_code] = mapping[scheme_code][-1]
            else:
                unresolved.append(scheme_code)
        return resolved, resolved_new_wpcs, unresolved

    @classmethod
    async def resolve_wpcs_from_tpsl_scheme_codes(cls, db: AsyncSession, tpsl_scheme_codes):
        resolved, resolved_new_wpcs, unresolved = {}, {}, []
        if not (tpsl_scheme_codes and isinstance(tpsl_scheme_codes, list)):
            return resolved, resolved_new_wpcs, unresolved
        mapping = await cls.get_tpsl_scheme_code_wpc_mapping_from_db(db, tpsl_scheme_codes)
        for tpsl_scheme_code in tpsl_scheme_codes:
            if mapping.get(tpsl_scheme_code):
                wpc = mapping[tpsl_scheme_code][0]
                resolved[tpsl_scheme_code] = wpc
                if len(mapping[tpsl_scheme_code]) > 1:
                    resolved_new_wpcs[tpsl_scheme_code] = mapping[tpsl_scheme_code][-1]
            else:
                unresolved.append(tpsl_scheme_code)
        return resolved, resolved_new_wpcs, unresolved

    @classmethod
    async def update_all_mappings_for_scheme(cls, db: AsyncSession, obj, target_wpc=None):
        if not obj:
            return
        wpc = target_wpc or obj.wpc
        if not wpc:
            return
        wschemecode = obj.wschemecode
        isin = obj.isin
        scheme_code = obj.scheme_code
        tpsl_scheme_code = obj.tpsl_scheme_code
        if wschemecode and not await db.execute(select(WSchemeCodeWPCMapping).filter_by(wschemecode=wschemecode, wpc=wpc)).first():
            db.add(WSchemeCodeWPCMapping(wschemecode=wschemecode, wpc=wpc))
        if isin and not await db.execute(select(ISINWPCMapping).filter_by(isin=isin, wpc=wpc)).first():
            db.add(ISINWPCMapping(isin=isin, wpc=wpc))
        if not obj.isin_reinvestment and scheme_code and not await db.execute(select(SchemeCodeWPCMapping).filter_by(scheme_code=scheme_code, wpc=wpc)).first():
            db.add(SchemeCodeWPCMapping(scheme_code=scheme_code, wpc=wpc))
        elif obj.isin_reinvestment and scheme_code and not await db.execute(select(SchemeCodeWPCMapping).filter_by(scheme_code=scheme_code)).first():
            db.add(SchemeCodeWPCMapping(scheme_code=scheme_code, wpc=wpc))
        if (tpsl_scheme_code != scheme_code or not obj.isin_reinvestment) and tpsl_scheme_code and not await db.execute(select(TPSLSchemeCodeWPCMapping).filter_by(tpsl_scheme_code=tpsl_scheme_code, wpc=wpc)).first():
            db.add(TPSLSchemeCodeWPCMapping(tpsl_scheme_code=tpsl_scheme_code, wpc=wpc))
        if (tpsl_scheme_code != scheme_code and obj.isin_reinvestment) and tpsl_scheme_code and not await db.execute(select(TPSLSchemeCodeWPCMapping).filter_by(tpsl_scheme_code=tpsl_scheme_code)).first():
            db.add(TPSLSchemeCodeWPCMapping(tpsl_scheme_code=tpsl_scheme_code, wpc=wpc))
        await db.commit()

    @classmethod
    async def update_all_mappings_for_schemes(cls, db: AsyncSession, objs):
        if not objs:
            return
        for obj in objs:
            await cls.update_all_mappings_for_scheme(db, obj)

'''
