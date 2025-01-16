from sqlmodel import Field, SQLModel, Enum, JSON, Index, UniqueConstraint, PrimaryKeyConstraint  # Replace SQLAlchemy imports with SQLModel imports
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func
from sqlalchemy import Column, String, JSON  # Add Column import from sqlalchemy
from app.db.base import Base
from app.utils.constants import DivTypeChoices
from app.utils.futils import is_env_prod
from app.utils.tasks import update_mappings_for_scheme_task, reset_cache_keys_affected_by_scheme_update_task
from app.utils.model_utils import WealthyProductCodeField, WealthyExternalIdField, generate_wealthy_mf_code
from enum import Enum as PyEnum
from decimal import Decimal
import pytz
from datetime import datetime
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import JSONB
from typing import Dict

class SchemeType(PyEnum):
    OPEN_ENDED = 'OE'
    CLOSE_ENDED = 'CE'
    INTERVAL = 'IN'

class LockInUnitType(PyEnum):
    Days = 'D'
    Months = 'M'
    Years = 'Y'

class SchemeIDGenerator(BaseModel, table=True):
    __tablename__ = "funnal_schemeidgenerator"
    generated_id: int = Field(primary_key=True)

class Scheme(BaseModel, table=True):
    __tablename__ = "funnal_scheme"
    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
        
    wschemecode: str = Field(max_length=28, primary_key=True)
    wpc: str = WealthyProductCodeField(prefix="MF", Modal=SchemeIDGenerator, max_length=12, unique=True, nullable=True)
    third_party_id: str = Field(max_length=10, nullable=True)
    isin: str = Field(max_length=20, nullable=True)
    isin_reinvestment: str = Field(max_length=20, nullable=True)
    third_party_amc: str = Field(max_length=10, nullable=True)
    class_code: str = Field(max_length=10, nullable=True)
    amfi_code: str = Field(max_length=20, nullable=True)
    scheme_code: str = Field(max_length=20, nullable=True)
    scheme_code_ptm: str = Field(max_length=20, nullable=True)
    scheme_code_dtm: str = Field(max_length=20, nullable=True)
    tpsl_scheme_code: str = Field(max_length=20, nullable=True)
    fund_family_code: str = Field(max_length=50, nullable=True)
    scheme_name: str = Field(max_length=255, nullable=True)
    benchmark: str = Field(max_length=255, nullable=True)
    benchmark_tpid: str = Field(max_length=10, nullable=True)
    display_name: str = Field(max_length=255, nullable=True)
    category: str = Field(max_length=255, nullable=True)
    scheme_type: str = Field(max_length=2, nullable=True)
    aum: Decimal = Field(nullable=True, max_digits=20, decimal_places=4)
    lock_in_time: int = Field(nullable=True)
    lock_in_unit: str = Field(max_length=2, nullable=True)
    risk_o_meter_value: str = Field(max_length=50, nullable=True)
    fund_manager: str = Field(max_length=100, nullable=True)
    fund_manager_profile: str = Field(nullable=True)
    objective: str = Field(nullable=True)
    frequency: str = Field(max_length=100, nullable=True)
    max_deposit_amt: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    min_deposit_amt: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    min_add_deposit_amt: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    min_sip_deposit_amt: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    min_withdrawal_amt: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    max_one_day_investment: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    max_monthly_investment: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    max_sip_monthly_investment: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    max_stp_one_day_investment: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    max_stp_weekly_investment: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    max_stp_monthly_investment: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    total_no_of_sips_allowed: int = Field(nullable=True)
    max_monthly_investment_per_pan: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    nri_investment_allowed: bool = Field(default=False)
    nav: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    adj_nav: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    nav_at_launch: Decimal = Field(default=10.000000, max_digits=20, decimal_places=6)
    nav_date: datetime = Field(nullable=True)
    latest_diff: Decimal = Field(default=0.000, max_digits=20, decimal_places=3)
    latest_percentage_change: Decimal = Field(default=0.000, max_digits=20, decimal_places=3)
    return_type: str = Field(max_length=2, nullable=True)
    plan_type: str = Field(max_length=2, nullable=True)
    scheme_nature: str = Field(max_length=2, nullable=True)
    fund_type: str = Field(max_length=2, nullable=True)
    amc: str = Field(max_length=3, nullable=True)
    exit_load_time: int = Field(nullable=True)
    exit_load_unit: str = Field(max_length=2, nullable=True)
    exit_load_percentage: Decimal = Field(nullable=True, max_digits=10, decimal_places=6)
    exit_load_remarks: str = Field(nullable=True)
    latest_hnav_date: datetime = Field(nullable=True)
    taxation_type: str = Field(max_length=2, nullable=True)
    taxation_type_remarks: str = Field(max_length=254, nullable=True)
    face_value: Decimal = Field(nullable=True, max_digits=10, decimal_places=2)
    trynor_ratio: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    sharpe: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    information_ratio: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    alpha: Decimal = Field(nullable=True, max_digits=20, decimal_places=3)
    beta: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    sd: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    pe: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    returns_one_week: Decimal = Field(nullable=True, max_digits=20, decimal_places=3)
    returns_one_month: Decimal = Field(nullable=True, max_digits=20, decimal_places=3)
    returns_three_months: Decimal = Field(nullable=True, max_digits=20, decimal_places=3)
    returns_six_months: Decimal = Field(nullable=True, max_digits=20, decimal_places=3)
    returns_one_year: Decimal = Field(nullable=True, max_digits=20, decimal_places=3)
    returns_three_years: Decimal = Field(nullable=True, max_digits=20, decimal_places=3)
    returns_five_years: Decimal = Field(nullable=True, max_digits=20, decimal_places=3)
    returns_since_inception: Decimal = Field(nullable=True, max_digits=20, decimal_places=3)
    rank_in_category_1_year: str = Field(max_length=10, nullable=True)
    rank_in_category_3_year: str = Field(max_length=10, nullable=True)
    rank_in_category_5_year: str = Field(max_length=10, nullable=True)
    expense_ratio: Decimal = Field(default=0.000000, max_digits=20, decimal_places=6)
    debt_equity_ratio: str = Field(max_length=10, nullable=True)
    prev_debt_equity_ratio: str = Field(max_length=10, nullable=True)
    asset_allocation: dict = Field(sa_column=Column(JSONB), default_factory=dict)
    yield_till_maturity: Decimal = Field(default=0.000000, max_digits=20, decimal_places=6)
    maturity_date: datetime = Field(nullable=True)
    modified_duration: Decimal = Field(default=0.000000, max_digits=10, decimal_places=3)
    macaulay_duration: Decimal = Field(default=0.000000, max_digits=10, decimal_places=3)
    aaa_sovereign_allocation: Decimal = Field(default=0.000000, max_digits=10, decimal_places=6)
    holding_in_top_20_companies: Decimal = Field(default=0.000000, max_digits=10, decimal_places=6)
    launch_date: datetime = Field(nullable=True)
    close_date: datetime = Field(nullable=True)
    allotment_date: datetime = Field(nullable=True)
    sip_registration_start_date: datetime = Field(nullable=True)
    sip_registration_end_date: datetime = Field(nullable=True)
    dividend_yield: Decimal = Field(default=0.000000, max_digits=20, decimal_places=6)
    rta: str = Field(max_length=30, nullable=True)
    rta_product_code: str = Field(max_length=30, nullable=True)
    rta_amc_code: str = Field(max_length=30, nullable=True)
    rta_scheme_code: str = Field(max_length=30, nullable=True)
    rta_plan_code: str = Field(max_length=30, nullable=True)
    rta_option_code: str = Field(max_length=30, nullable=True)
    payment_blocked_from: datetime = Field(nullable=True)
    payment_blocked_till: datetime = Field(nullable=True)
    payment_blocked_reason: str = Field(max_length=254, nullable=True)
    suspended_at: datetime = Field(nullable=True)
    exchange_traded: bool = Field(nullable=True)
    exchange_listed: bool = Field(nullable=True)
    advisory_approved: bool = Field(default=False)
    physical_mode: bool = Field(default=True)
    demat_mode: bool = Field(default=True)
    lumpsum_allowed: bool = Field(default=True)
    sip_allowed: bool = Field(default=True)
    hidden: bool = Field(default=False)
    ir_scheme: bool = Field(default=False)
    deprecated_at: datetime = Field(nullable=True)
    deprecate_reason: str = Field(max_length=254, nullable=True)
    w_rating: Decimal = Field(default=0.000000, max_digits=6, decimal_places=4)
    w_score: Decimal = Field(default=0.000000, max_digits=6, decimal_places=4)
    w_return_score: Decimal = Field(default=0.000000, max_digits=6, decimal_places=4)
    w_risk_score: Decimal = Field(default=0.000000, max_digits=6, decimal_places=4)
    w_valuation_score: Decimal = Field(default=0.000000, max_digits=6, decimal_places=4)
    w_credit_quality_score: Decimal = Field(default=0.000000, max_digits=6, decimal_places=4)
    ratings_as_on: datetime = Field(nullable=True)
    wealthy_select: bool = Field(default=False)

    __table_args__ = (
        Index('ix_scheme_third_party_id', 'third_party_id'),
        Index('ix_scheme_isin', 'isin'),
        Index('ix_scheme_amfi_code', 'amfi_code'),
        Index('ix_scheme_scheme_code', 'scheme_code'),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'wschemecode' not in kwargs or not kwargs['wschemecode']:
            self.wschemecode = generate_wealthy_mf_code(self)

    def save(self, session: Session):
        if not self.wschemecode:
            self.wschemecode = generate_wealthy_mf_code(self)
        session.add(self)
        session.commit()
        if not is_env_prod():
            return
        update_mappings_for_scheme_task.delay(self.wpc)
        reset_cache_keys_affected_by_scheme_update_task.delay(self.wpc)

    @property
    def is_tax_saver(self):
        if not self.category:
            return False
        return "elss" in str(self.category).lower()

    @property
    def is_payment_allowed(self):
        if self.deprecated_at:
            return False
        if self.close_date and self.sip_registration_start_date:
            indian_tz = pytz.timezone('Asia/Kolkata')
            now = datetime.now().astimezone(indian_tz).date()
            if self.close_date <= now <= self.sip_registration_start_date:
                return False
        if not (self.payment_blocked_from or self.payment_blocked_till):
            return True
        now = datetime.now().date()
        if self.payment_blocked_from and self.payment_blocked_till:
            if self.payment_blocked_from <= now <= self.payment_blocked_till:
                return False
            return True
        if self.payment_blocked_from:
            if now >= self.payment_blocked_from:
                return False
            return True
        if self.payment_blocked_till:
            if now <= self.payment_blocked_till:
                return False
            return True
        return True

    @property
    def dynamic_payment_blocked_reason(self):
        if self.deprecated_at:
            return self.payment_blocked_reason or "Fund has been deprecated"
        if self.close_date and self.sip_registration_start_date:
            indian_tz = pytz.timezone('Asia/Kolkata')
            now = datetime.now().astimezone(indian_tz).date()
            if self.close_date <= now <= self.sip_registration_start_date:
                return self.payment_blocked_reason or 'Investment is currently not allowed in this NFO'
        return self.payment_blocked_reason

class SchemeAudit(BaseModel, table=True):
    __tablename__ = "funnal_schemeaudit"
    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
    id: int = Field(primary_key=True)
    wpc: str = Field(max_length=12, nullable=True)
    wschemecode: str = Field(max_length=28, nullable=True)
    isin: str = Field(max_length=20, nullable=True)
    third_party_amc: str = Field(max_length=10, nullable=True)
    amfi_code: str = Field(max_length=20, nullable=True)
    scheme_code: str = Field(max_length=20, nullable=True)
    tpsl_scheme_code: str = Field(max_length=20, nullable=True)
    fund_family_code: str = Field(max_length=50, nullable=True)
    scheme_name: str = Field(max_length=255, nullable=True)
    benchmark: str = Field(max_length=255, nullable=True)
    category: str = Field(max_length=255, nullable=True)
    scheme_type: str = Field(max_length=2, nullable=True)
    aum: Decimal = Field(nullable=True, max_digits=20, decimal_places=4)
    lock_in_time: int = Field(nullable=True)
    lock_in_unit: str = Field(max_length=2, nullable=True)
    risk_o_meter_value: str = Field(max_length=50, nullable=True)
    fund_manager: str = Field(max_length=100, nullable=True)
    frequency: str = Field(max_length=100, nullable=True)
    max_deposit_amt: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    min_deposit_amt: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    min_add_deposit_amt: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    min_sip_deposit_amt: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    min_withdrawal_amt: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    #daily max investment in a fund
    max_one_day_investment: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    max_monthly_investment: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    max_sip_monthly_investment: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    max_stp_one_day_investment: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    max_stp_weekly_investment: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    max_stp_monthly_investment: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    total_no_of_sips_allowed: int = Field(nullable=True)
    max_monthly_investment_per_pan: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    nri_investment_allowed: bool = Field(default=False)
    return_type: str = Field(max_length=2, nullable=True)
    plan_type: str = Field(max_length=2, nullable=True)
    scheme_nature: str = Field(max_length=2, nullable=True)
    fund_type: str = Field(max_length=2, nullable=True)
    amc: str = Field(max_length=3, nullable=True)
    exit_load_time: int = Field(nullable=True)
    exit_load_unit: str = Field(max_length=2, nullable=True)
    exit_load_percentage: Decimal = Field(nullable=True, max_digits=10, decimal_places=6)
    exit_load_remarks: str = Field(nullable=True)
    taxation_type: str = Field(max_length=2, nullable=True)
    taxation_type_remarks: str = Field(max_length=254, nullable=True)
    expense_ratio: Decimal = Field(nullable=True, max_digits=20, decimal_places=6)
    maturity_date: datetime = Field(nullable=True)
    sip_registration_start_date: datetime = Field(nullable=True)
    sip_registration_end_date: datetime = Field(nullable=True)
    payment_blocked_from: datetime = Field(nullable=True)
    payment_blocked_till: datetime = Field(nullable=True)
    suspended_at: datetime = Field(nullable=True)
    advisory_approved: bool = Field(nullable=True)
    physical_mode: bool = Field(nullable=True)
    demat_mode: bool = Field(nullable=True)
    lumpsum_allowed: bool = Field(nullable=True)
    sip_allowed: bool = Field(nullable=True)
    hidden: bool = Field(nullable=True)
    deprecated_at: datetime = Field(nullable=True)
    deprecate_reason: str = Field(max_length=254, nullable=True)
    requestor_code: str = Field(nullable=True)

    @property
    def is_payment_allowed(self):
        if self.deprecated_at:
            return False
        if not (self.payment_blocked_from or self.payment_blocked_till):
            return True
        now = func.now().date()
        if self.payment_blocked_from and self.payment_blocked_till:
            if self.payment_blocked_from <= now <= self.payment_blocked_till:
                return False
            return True
        if self.payment_blocked_from:
            if now >= self.payment_blocked_from:
                return False
            return True
        if self.payment_blocked_till:
            if now <= self.payment_blocked_till:
                return False
            return True
        return True

    @property
    def display_name(self):
        return self.scheme_name

    __table_args__ = (
        Index('ix_sa_scheme_code_37', 'scheme_code'),
        Index('ix_sa_isin_90', 'isin'),
        Index('ix_sa_wsc_8612', 'wschemecode'),
        Index('ix_sa_category_79', 'category'),
    )

class SchemeHolding(BaseModel, table=True):
    __tablename__ = "funnal_schemeholding"
    class Config:
        arbitrary_types_allowed = True
    external_id: str = WealthyExternalIdField(prefix="sch_holding_", primary_key=True)
    wpc: str = Field(max_length=12)
    portfolio_date: datetime = Field()
    holding_third_party_id: str = Field(max_length=10, nullable=False)
    holding_trading_symbol: str = Field(max_length=50, nullable=True)
    holding_name: str = Field(max_length=254, nullable=False)
    holding_percentage: Decimal = Field(nullable=False, max_digits=9, decimal_places=6)
    market_value: Decimal = Field(nullable=False, max_digits=20, decimal_places=4)
    no_of_shares: int = Field(nullable=False)
    sector_name: str = Field(max_length=70, nullable=False)
    asset_type: str = Field(max_length=70, nullable=False)
    rating: str = Field(max_length=15, nullable=False)
    wrating: str = Field(max_length=15, nullable=True)
    rating_agency: str = Field(max_length=100, nullable=True)
    isin: str = Field(max_length=20, nullable=True)
    reported_sector: str = Field(max_length=70, nullable=True)

    __table_args__ = (
        Index('idx_sh_wpc_876', 'wpc'),
        Index('idx_sh_htpid_564', 'holding_third_party_id'),
        Index('idx_sh_sector_267', 'sector_name'),
        Index('idx_sh_rating_391', 'rating'),
        UniqueConstraint('wpc', 'holding_third_party_id', 'isin', name='uq_scheme_holding'),
    )

class WSchemeCodeWPCMapping(BaseModel, table=True):
    __tablename__ = "funnal_wschemecodewpcmapping"

    wschemecode: str = Field(max_length=28)
    external_id: str = WealthyExternalIdField(prefix="wsc_wpc_map_", primary_key=True)
    wpc: str = Field(max_length=12, nullable=False)
    hidden: bool = Field(default=False)

    __table_args__ = (
        Index('ix_wwm_wsc_610', 'wschemecode'),
        Index('ix_swm_wpc_941', 'wpc')
    )


class SchemeCodeWPCMapping(BaseModel, table=True):
    __tablename__ = "funnal_schemecodewpcmapping"
    
    external_id: str = WealthyExternalIdField(prefix="sc_wpc_map_", primary_key=True)
    scheme_code: str = Field(max_length=20)
    wpc: str = Field(max_length=12)
#    order: int = Field(default=1)
    hidden: bool = Field(default=False)
#    div_type: DivTypeChoices = Field(sa_column=Column(String, nullable=True))

    __table_args__ = (
        UniqueConstraint('scheme_code', 'wpc', name='uq_scheme_code_wpc'),
        Index('ix_swm_sc_428', 'scheme_code'),
        Index('ix_swm_wpc_941', 'wpc'),
    )

    @staticmethod
    def validate_div_type(value: str) -> str:
        if value not in DivTypeChoices._value2member_map_:
            raise ValueError(f"Invalid div_type: {value}")
        return value

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.div_type = Field(sa_column=Column(String, nullable=True), validator=cls.validate_div_type)

class ParentChildSchemeMapping(BaseModel, table=True):
    __tablename__ = "funnal_parentchildschememapping"

    external_id: str = WealthyExternalIdField(prefix="par_ch_sch_map_", primary_key=True)
    child_wpc: str = Field(max_length=12, nullable=False)
    parent_wpc: str = Field(max_length=12, nullable=False)

    __table_args__ = (
        UniqueConstraint('child_wpc', 'parent_wpc', name='uq_child_parent_wpc'),
        Index('ix_prs_cwpc_981', 'child_wpc'),
        Index('ix_prc_pwpc_728', 'parent_wpc'),
    )

class SectorToWSectorMapping(BaseModel, table=True):
    __tablename__ = "funnal_sectortowsectormapping"

    external_id: str = WealthyExternalIdField(prefix="sctwsc_map_", primary_key=True)
    sector: str = Field(max_length=60, unique=True)
    wsector: str = Field(max_length=35)

    __table_args__ = (
        Index('ix_stwm_sct_587', 'sector'),
        Index('ix_stwm_wsct_785', 'wsector'),
    )

class SchemeHistNavData(BaseModel, table=True):
    __tablename__ = "funnal_schemehistnavdata"
    id: int = Field(primary_key=True)
    wpc: str = Field(max_length=12, nullable=False)
    nav_date: datetime = Field(nullable=False)
    nav: Decimal = Field(default=0.000000, nullable=False, max_digits=20, decimal_places=6)
    adj_nav: Decimal = Field(default=0.000000, nullable=False, max_digits=20, decimal_places=6)
    diff: Decimal = Field(default=0.000000, nullable=False, max_digits=20, decimal_places=6)
    percentage_change: Decimal = Field(default=0.000000, nullable=False, max_digits=20, decimal_places=6)

    __table_args__ = (
        UniqueConstraint('wpc', 'nav_date', name='uq_scheme_hist_nav_data_wpc_nav_date'),
        Index('idx_shnd_wpc_324', 'wpc'),
    )

class WPCToTWPCMapping(BaseModel, table=True):
    __tablename__ = "funnal_wpctotwpcmapping"

    external_id: str = WealthyExternalIdField(prefix="wpc_wpc_map_", primary_key=True)
    wpc: str = Field(max_length=12, nullable=False)
    target_wpc: str = Field(max_length=12, nullable=False)
    hidden: bool = Field(default=False)

    __table_args__ = (
        UniqueConstraint('wpc', 'target_wpc', name='uq_wpc_target_wpc'),
        Index('ix_wwm_wpc_674', 'wpc'),
        Index('ix_wwm_twpc_292', 'target_wpc'),
    )

class ISINWPCMapping(BaseModel, table=True):
    __tablename__ = "funnal_isinwpcmapping"

    external_id: str = WealthyExternalIdField(prefix="isin_wpc_map_", primary_key=True)
    isin: str = Field(max_length=20, nullable=False)
    wpc: str = Field(max_length=12, nullable=False)
    hidden: bool = Field(default=False)

    __table_args__ = (
        UniqueConstraint('isin', 'wpc', name='uq_isin_wpc'),
        Index('ix_iwm_isin_823', 'isin'),
        Index('ix_iwm_wpc_591', 'wpc'),
    )