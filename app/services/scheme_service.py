from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from app.models.scheme_models import Scheme, SchemeHolding
from app.crud.scheme_crud import SchemeCreate, SchemeUpdate, SchemeHoldingCreate
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal

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

    @staticmethod
    def get_scheme_holdings(db: Session, wpc: str) -> List[SchemeHolding]:
        return db.query(SchemeHolding).filter(SchemeHolding.wpc == wpc).all()

    @staticmethod
    def create_scheme_holding(db: Session, holding: SchemeHoldingCreate) -> SchemeHolding:
        db_holding = SchemeHolding(**holding.dict())
        db.add(db_holding)
        db.commit()
        db.refresh(db_holding)
        return db_holding

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