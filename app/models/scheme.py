from sqlalchemy import Column, String, Boolean, Numeric, Date, DateTime, ForeignKey, Index, Integer, Text, Enum, JSON, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship,Session
from sqlalchemy.sql import func
from app.db.base import Base
from app.utils.futils import is_env_prod
from app.utils.tasks import update_mappings_for_scheme_task, reset_cache_keys_affected_by_scheme_update_task
from app.utils.model_utils import WealthyProductCodeField, WealthyExternalIdField,generate_wealthy_mf_code
from enum import Enum as PyEnum
from decimal import Decimal
import pytz
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

class SchemeType(PyEnum):
    OPEN_ENDED = 'OE'
    CLOSE_ENDED = 'CE'
    INTERVAL = 'IN'

class LockInUnitType(PyEnum):
    Days = 'D'
    Months = 'M'
    Years = 'Y'

class SchemeIDGenerator(Base):
    __tablename__ = "funnal_schemeidgenerator"
    generated_id = Column(Integer, primary_key=True, autoincrement=True)



class Scheme(Base):
    __tablename__ = "funnal_scheme"

    wschemecode = Column(String(28), primary_key=True)
    wpc =   WealthyProductCodeField(prefix="MF", Modal=SchemeIDGenerator, max_length=12)
    third_party_id = Column(String(10), nullable=True)  # CMOTS equivalent mf_cocode, used to determine amc
    isin = Column(String(20), nullable=True)
    isin_reinvestment = Column(String(20), nullable=True)
    third_party_amc = Column(String(10), nullable=True)  # CMOTS equivalent mf_cocode, used to determine amc
    class_code = Column(String(10), nullable=True)  # specific to CMOTS, needed in CMOTS scheme returns API
    amfi_code = Column(String(20), nullable=True)
    scheme_code = Column(String(20), nullable=True)
    scheme_code_ptm = Column(String(20), nullable=True)  # ptm - physical transaction mode
    scheme_code_dtm = Column(String(20), nullable=True)  # dtm - demat transaction mode
    tpsl_scheme_code = Column(String(20), nullable=True)
    fund_family_code = Column(String(50), nullable=True)
    scheme_name = Column(String(255), nullable=True)
    benchmark = Column(String(255), nullable=True)
    benchmark_tpid = Column(String(10), nullable=True)
    display_name = Column(String(255), nullable=True)
    category = Column(String(255), nullable=True)
    scheme_type = Column(String(2), nullable=True)
    aum = Column(Numeric(20, 4), nullable=True)
    lock_in_time = Column(Integer, nullable=True)  # receiving always in years from CMOTS
    lock_in_unit = Column(String(2), nullable=True)
    risk_o_meter_value = Column(String(50), nullable=True)
    fund_manager = Column(String(100), nullable=True)
    fund_manager_profile = Column(String, nullable=True)
    objective = Column(String, nullable=True)
    frequency = Column(String(100), nullable=True)
    max_deposit_amt = Column(Numeric(20, 6), nullable=True)
    min_deposit_amt = Column(Numeric(20, 6), nullable=True)
    min_add_deposit_amt = Column(Numeric(20, 6), nullable=True)
    min_sip_deposit_amt = Column(Numeric(20, 6), nullable=True)
    min_withdrawal_amt = Column(Numeric(20, 6), nullable=True)
    max_one_day_investment = Column(Numeric(20, 6), nullable=True)  # Daily Max investment in a Fund
    max_monthly_investment = Column(Numeric(20, 6), nullable=True)  # Max investment in a month
    max_sip_monthly_investment = Column(Numeric(20, 6), nullable=True)
    max_stp_one_day_investment = Column(Numeric(20, 6), nullable=True)
    max_stp_weekly_investment = Column(Numeric(20, 6), nullable=True)
    max_stp_monthly_investment = Column(Numeric(20, 6), nullable=True)
    total_no_of_sips_allowed = Column(Integer, nullable=True)  # Total sips allowed.
    max_monthly_investment_per_pan = Column(Numeric(20, 6), nullable=True)  # Monthly investment pan-wise per month.
    nri_investment_allowed = Column(Boolean, default=False)  # Is NRI investment allowed.
    nav = Column(Numeric(20, 6), nullable=True)
    adj_nav = Column(Numeric(20, 6), nullable=True)
    nav_at_launch = Column(Numeric(20, 6), default=10.000000)
    nav_date = Column(DateTime, nullable=True)
    latest_diff = Column(Numeric(20, 3), default=0.000)
    latest_percentage_change = Column(Numeric(20, 3), default=0.000)
    return_type = Column(String(2), nullable=True)  # InvestmentType
    plan_type = Column(String(2), nullable=True)  # SchemeInvestmentType
    scheme_nature = Column(String(2), nullable=True)  # open/close ended, FundType
    fund_type = Column(String(2), nullable=True)  # MainCategory
    amc = Column(String(3), nullable=True)  # use cmots_amc_mapping to figure out this value
    exit_load_time = Column(Integer, nullable=True)
    exit_load_unit = Column(String(2), nullable=True)
    exit_load_percentage = Column(Numeric(10, 6), nullable=True)
    exit_load_remarks = Column(String, nullable=True)
    latest_hnav_date = Column(DateTime, nullable=True)
    taxation_type = Column(String(2), nullable=True)
    taxation_type_remarks = Column(String(254), nullable=True)
    face_value = Column(Numeric(10, 2), nullable=True)
    trynor_ratio = Column(Numeric(20, 6), nullable=True)
    sharpe = Column(Numeric(20, 6), nullable=True)
    information_ratio = Column(Numeric(20, 6), nullable=True)
    alpha = Column(Numeric(20, 3), nullable=True)
    beta = Column(Numeric(20, 6), nullable=True)
    sd = Column(Numeric(20, 6), nullable=True)
    pe = Column(Numeric(20, 6), nullable=True)
    returns_one_week = Column(Numeric(20, 3), nullable=True)
    returns_one_month = Column(Numeric(20, 3), nullable=True)
    returns_three_months = Column(Numeric(20, 3), nullable=True)
    returns_six_months = Column(Numeric(20, 3), nullable=True)
    returns_one_year = Column(Numeric(20, 3), nullable=True)
    returns_three_years = Column(Numeric(20, 3), nullable=True)
    returns_five_years = Column(Numeric(20, 3), nullable=True)
    returns_since_inception = Column(Numeric(20, 3), nullable=True)
    rank_in_category_1_year = Column(String(10), nullable=True)  # to be computed
    rank_in_category_3_year = Column(String(10), nullable=True)  # to be computed
    rank_in_category_5_year = Column(String(10), nullable=True)  # to be computed
    expense_ratio = Column(Numeric(20, 6), default=0.000000)  # https://wealthyapis.cmots.com/api/SchemeProfileExpRatio
    debt_equity_ratio = Column(String(10), nullable=True)
    prev_debt_equity_ratio = Column(String(10), nullable=True)
    asset_allocation = Column(JSON, nullable=True)  # json
    yield_till_maturity = Column(Numeric(20, 6), default=0.000000)  # (same as YTM)
    maturity_date = Column(DateTime, nullable=True)  # getting it from SchemeMaster API
    modified_duration = Column(Numeric(10, 3), default=0.000000)  # (same as ModDuration)
    macaulay_duration = Column(Numeric(10, 3), default=0.000000)  # (same as MacaulayDuration)
    aaa_sovereign_allocation = Column(Numeric(10, 6), default=0.000000)
    holding_in_top_20_companies = Column(Numeric(10, 6), default=0.000000)
    launch_date = Column(DateTime, nullable=True)
    close_date = Column(DateTime, nullable=True)
    allotment_date = Column(DateTime, nullable=True)
    sip_registration_start_date = Column(DateTime, nullable=True)  # alias reopening_date
    sip_registration_end_date = Column(DateTime, nullable=True)
    dividend_yield = Column(Numeric(20, 6), default=0.000000)  # yet to be figured
    rta = Column(String(30), nullable=True)
    rta_product_code = Column(String(30), nullable=True)
    rta_amc_code = Column(String(30), nullable=True)
    rta_scheme_code = Column(String(30), nullable=True)
    rta_plan_code = Column(String(30), nullable=True)
    rta_option_code = Column(String(30), nullable=True)
    payment_blocked_from = Column(DateTime, nullable=True)
    payment_blocked_till = Column(DateTime, nullable=True)
    payment_blocked_reason = Column(String(254), nullable=True)
    suspended_at = Column(DateTime, nullable=True)
    exchange_traded = Column(Boolean, nullable=True)
    exchange_listed = Column(Boolean, nullable=True)
    advisory_approved = Column(Boolean, default=False)
    physical_mode = Column(Boolean, default=True)
    demat_mode = Column(Boolean, default=True)
    lumpsum_allowed = Column(Boolean, default=True)
    sip_allowed = Column(Boolean, default=True)
    hidden = Column(Boolean, default=False)
    ir_scheme = Column(Boolean, default=False)
    deprecated_at = Column(DateTime, nullable=True)
    deprecate_reason = Column(String(254), nullable=True)
    w_rating = Column(Numeric(6, 4), default=0.000000)
    w_score = Column(Numeric(6, 4), default=0.000000)
    w_return_score = Column(Numeric(6, 4), default=0.000000)
    w_risk_score = Column(Numeric(6, 4), default=0.000000)
    w_valuation_score = Column(Numeric(6, 4), default=0.000000)
    w_credit_quality_score = Column(Numeric(6, 4), default=0.000000)
    ratings_as_on = Column(DateTime, nullable=True)
    wealthy_select = Column(Boolean, default=False)

    __table_args__ = (
        Index('ix_scheme_third_party_id', 'third_party_id'),
        Index('ix_scheme_isin', 'isin'),
        Index('ix_scheme_amfi_code', 'amfi_code'),
        Index('ix_scheme_scheme_code', 'scheme_code'),
    )

    def __init__(self, **kwargs):
        super(Scheme, self).__init__(**kwargs)
        if 'wschemecode' not in kwargs or not kwargs['wschemecode']:
            self.wschemecode = generate_wealthy_mf_code(self)

    def save(self, session: Session, force_insert=False, force_update=False, using=None, update_fields=None):
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
        # both are empty
        if not (self.payment_blocked_from or self.payment_blocked_till):
            return True
        now = datetime.now().date()
        # both are present
        if self.payment_blocked_from and self.payment_blocked_till:
            if self.payment_blocked_from <= now <= self.payment_blocked_till:
                return False
            return True
        # only payment_blocked_from is present
        if self.payment_blocked_from:
            if now >= self.payment_blocked_from:
                return False
            return True
        # only payment_blocked_till is present
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



class SchemeAudit(Base):
    __tablename__ = "funnal_schemeaudit"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wpc = Column(String(12), nullable=True)
    wschemecode = Column(String(28), nullable=True)
    isin = Column(String(20), nullable=True)
    third_party_amc = Column(String(10), nullable=True)  # CMOTS equivalent mf_cocode, used to determine amc
    amfi_code = Column(String(20), nullable=True)
    scheme_code = Column(String(20), nullable=True)
    tpsl_scheme_code = Column(String(20), nullable=True)
    fund_family_code = Column(String(50), nullable=True)
    scheme_name = Column(String(255), nullable=True)
    benchmark = Column(String(255), nullable=True)
    category = Column(String(255), nullable=True)
    scheme_type = Column(String(2), nullable=True)
    aum = Column(Numeric(20, 4), nullable=True)
    lock_in_time = Column(Integer, nullable=True)  # receiving always in years from CMOTS
    lock_in_unit = Column(String(2), nullable=True)
    risk_o_meter_value = Column(String(50), nullable=True)
    fund_manager = Column(String(100), nullable=True)
    frequency = Column(String(100), nullable=True)
    max_deposit_amt = Column(Numeric(20, 6), nullable=True)
    min_deposit_amt = Column(Numeric(20, 6), nullable=True)
    min_add_deposit_amt = Column(Numeric(20, 6), nullable=True)
    min_sip_deposit_amt = Column(Numeric(20, 6), nullable=True)
    min_withdrawal_amt = Column(Numeric(20, 6), nullable=True)
    max_one_day_investment = Column(Numeric(20, 6), nullable=True)  # Daily Max investment in a Fund
    max_monthly_investment = Column(Numeric(20, 6), nullable=True)  # Max investment in a month
    max_sip_monthly_investment = Column(Numeric(20, 6), nullable=True)
    max_stp_one_day_investment = Column(Numeric(20, 6), nullable=True)
    max_stp_weekly_investment = Column(Numeric(20, 6), nullable=True)
    max_stp_monthly_investment = Column(Numeric(20, 6), nullable=True)
    total_no_of_sips_allowed = Column(Integer, nullable=True)  # Total sips allowed.
    max_monthly_investment_per_pan = Column(Numeric(20, 6), nullable=True)  # Monthly investment pan-wise per month.
    nri_investment_allowed = Column(Boolean, default=False)  # Is NRI investment allowed.
    return_type = Column(String(2), nullable=True)  # InvestmentType
    plan_type = Column(String(2), nullable=True)  # SchemeInvestmentType
    scheme_nature = Column(String(2), nullable=True)  # open/close ended, FundType
    fund_type = Column(String(2), nullable=True)  # MainCategory
    amc = Column(String(3), nullable=True)  # use cmots_amc_mapping to figure out this value
    exit_load_time = Column(Integer, nullable=True)
    exit_load_unit = Column(String(2), nullable=True)
    exit_load_percentage = Column(Numeric(10, 6), nullable=True)
    exit_load_remarks = Column(Text, nullable=True)
    taxation_type = Column(String(2), nullable=True)
    taxation_type_remarks = Column(String(254), nullable=True)
    expense_ratio = Column(Numeric(20, 6), nullable=True)  # https://wealthyapis.cmots.com/api/SchemeProfileExpRatio
    maturity_date = Column(Date, nullable=True)  # getting it from SchemeMaster API
    sip_registration_start_date = Column(Date, nullable=True)
    sip_registration_end_date = Column(Date, nullable=True)
    payment_blocked_from = Column(Date, nullable=True)
    payment_blocked_till = Column(Date, nullable=True)
    suspended_at = Column(Date, nullable=True)
    advisory_approved = Column(Boolean, nullable=True)
    physical_mode = Column(Boolean, nullable=True)
    demat_mode = Column(Boolean, nullable=True)
    lumpsum_allowed = Column(Boolean, nullable=True)
    sip_allowed = Column(Boolean, nullable=True)
    hidden = Column(Boolean, nullable=True)
    deprecated_at = Column(DateTime, nullable=True)
    deprecate_reason = Column(String(254), nullable=True)
    requestor_code = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    #ideally etao chilo na dont know why eta add hoyeche
    #holdings = relationship("SchemeHolding", back_populates="scheme")
     
    @property
    def is_payment_allowed(self):
        if self.deprecated_at:
            return False
        # both are empty
        if not (self.payment_blocked_from or self.payment_blocked_till):
            return True
        now = func.now().date()
        # both are present
        if self.payment_blocked_from and self.payment_blocked_till:
            if self.payment_blocked_from <= now <= self.payment_blocked_till:
                return False
            return True
        # only payment_blocked_from is present
        if self.payment_blocked_from:
            if now >= self.payment_blocked_from:
                return False
            return True
        # only payment_blocked_till is present
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

class SchemeHolding(Base):
    __tablename__ = "funnal_schemeholding"

    external_id = Column(WealthyExternalIdField(prefix="sch_holding_"), primary_key=True)
    #wpc = Column(String(12), ForeignKey("schemes.wpc"))
    wpc = Column(String(12))
    portfolio_date = Column(Date)
    holding_third_party_id = Column(String(10), nullable=False)
    holding_trading_symbol = Column(String(50))
    holding_name = Column(String(254), nullable=False)
    holding_percentage = Column(Numeric(9, 6), nullable=False)
    market_value = Column(Numeric(20, 4), nullable=False)
    no_of_shares = Column(Integer, nullable=False)
    sector_name = Column(String(70), nullable=False)
    asset_type = Column(String(70), nullable=False)
    rating = Column(String(15), nullable=False)
    wrating = Column(String(15))
    rating_agency = Column(String(100))
    isin = Column(String(20))
    reported_sector = Column(String(70))

    ##scheme = relationship("Scheme", back_populates="holdings")

    __table_args__ = (
        Index('idx_sh_wpc_876', 'wpc'),
        Index('idx_sh_htpid_564', 'holding_third_party_id'),
        Index('idx_sh_sector_267', 'sector_name'),
        Index('idx_sh_rating_391', 'rating'),
        UniqueConstraint('wpc', 'holding_third_party_id', 'isin', name='uq_scheme_holding'),
    )

class WSchemeCodeWPCMapping(Base):
    __tablename__ = "funnal_wschemecodewpcmapping"
    __table_args__ = (
        Index('ix_swm_sc_428', 'scheme_code'),
        Index('ix_swm_wpc_941', 'wpc')
    )
    wschemecode = Column(String(28))
    external_id = Column(WealthyExternalIdField(prefix="sc_wpc_map_"), primary_key=True)
    scheme_code = Column(String(20), nullable=False)
    wpc = Column(String(12), nullable=False)
    hidden = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SchemeCodeWPCMapping(Base):
    __tablename__ = "funnal_schemecodewpcmapping"

    external_id = Column(WealthyExternalIdField(prefix="sc_wpc_map_"), primary_key=True)
    scheme_code = Column(String(20), nullable=False)
    wpc = Column(String(12), nullable=False)
    hidden = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
        Index('ix_swm_sc', 'scheme_code'),
        Index('ix_swm_wpc', 'wpc'),
    )


class ParentChildSchemeMapping(Base):
    __tablename__ = "funnal_parentchildschememapping"

    external_id = Column(WealthyExternalIdField(prefix="par_ch_sch_map_"), primary_key=True)
    child_wpc = Column(String(12), nullable=False)
    parent_wpc = Column(String(12), nullable=False)

    __table_args__ = (
        UniqueConstraint('child_wpc', 'parent_wpc', name='uq_child_parent_wpc'),
        Index('ix_prs_cwpc_981', 'child_wpc'),
        Index('ix_prc_pwpc_728', 'parent_wpc'),
    )

class SectorToWSectorMapping(Base):
    __tablename__ = "funnal_sectortowsectormapping"

    external_id = Column(WealthyExternalIdField(prefix="sctwsc_map_"), primary_key=True)
    sector = Column(String(60), unique=True)
    wsector = Column(String(35))

    __table_args__ = (
        Index('ix_stwm_sct_587', 'sector'),
        Index('ix_stwm_wsct_785', 'wsector'),
    )

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     cache_key = CacheKeysService.sector_to_wsector_mapping_cache_key()
    #     cache.delete(cache_key)
    #     super(SectorToWSectorMapping, self).save(
    #         force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields
    #     )
    
#Scheme.holdings = relationship("SchemeHolding", back_populates="scheme")



class SchemeHistNavData(Base):
    __tablename__ = "funnal_schemehistnavdata"

    wpc = Column(String(12), nullable=False)
    nav_date = Column(Date, nullable=False)
    nav = Column(Numeric(20, 6), default=0.000000, nullable=False)
    adj_nav = Column(Numeric(20, 6), default=0.000000, nullable=False)
    diff = Column(Numeric(20, 6), default=0.000000, nullable=False)
    percentage_change = Column(Numeric(20, 6), default=0.000000, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('wpc', 'nav_date', name='uq_scheme_hist_nav_data_wpc_nav_date'),
        Index('idx_shnd_wpc_324', 'wpc'),
    )
    
class WPCToTWPCMapping(Base):
    __tablename__ = "funnal_wpctotwpcmapping"

    external_id = Column(WealthyExternalIdField(prefix="wpc_wpc_map_"), primary_key=True)
    wpc = Column(String(12), nullable=False)
    target_wpc = Column(String(12), nullable=False)
    hidden = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint('wpc', 'target_wpc', name='uq_wpc_target_wpc'),
        Index('ix_wwm_wpc_674', 'wpc'),
        Index('ix_wwm_twpc_292', 'target_wpc'),
    )
    
class ISINWPCMapping(Base):
    __tablename__ = "funnal_isinwpcmapping"
    external_id = Column(WealthyExternalIdField(prefix="isin_wpc_map_", primary_key=True))
    isin = Column(String(20), nullable=False)
    wpc = Column(String(12), nullable=False)
    hidden = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('isin', 'wpc', name='uq_isin_wpc'),
        Index('ix_iwm_isin_823', 'isin'),
        Index('ix_iwm_wpc_591', 'wpc'),
    )