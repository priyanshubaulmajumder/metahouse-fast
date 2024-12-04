from pydantic_settings import BaseSettings, Field, field_validator
from typing import Optional, Dict
from decimal import Decimal
from datetime import date
from enum import Enum

# Import the necessary enums from your original schema file
from app.schemas.scheme import SchemeType, LockInUnitType, SchemeNature, MainCategory, ExitLoadUnitType, TaxationType

class SchemeCreate(BaseSettings):
    wschemecode: str
    wpc: str
    third_party_id: Optional[str] = None
    isin: Optional[str] = None
    isin_reinvestment: Optional[str] = None
    third_party_amc: Optional[str] = None
    class_code: Optional[str] = None
    amfi_code: Optional[str] = None
    scheme_code: Optional[str] = None
    scheme_code_ptm: Optional[str] = None
    scheme_code_dtm: Optional[str] = None
    tpsl_scheme_code: Optional[str] = None
    fund_family_code: Optional[str] = None
    scheme_name: Optional[str] = None
    benchmark: Optional[str] = None
    benchmark_tpid: Optional[str] = None
    display_name: Optional[str] = None
    category: Optional[str] = None
    scheme_type: Optional[SchemeType] = None
    aum: Optional[Decimal] = Field(None, decimal_places=4)
    lock_in_time: Optional[int] = None
    lock_in_unit: LockInUnitType = LockInUnitType.Years
    risk_o_meter_value: Optional[str] = None
    fund_manager: Optional[str] = None
    fund_manager_profile: Optional[str] = None
    objective: Optional[str] = None
    scheme_nature: SchemeNature = SchemeNature.Open
    fund_type: MainCategory = MainCategory.Equity
    amc: Optional[str] = None
    exit_load_time: Optional[int] = None
    exit_load_unit: ExitLoadUnitType = ExitLoadUnitType.Years
    exit_load_percentage: Optional[Decimal] = Field(None, decimal_places=6)
    exit_load_remarks: Optional[str] = None
    latest_hnav_date: Optional[date] = None
    taxation_type: Optional[TaxationType] = None
    debt_equity_ratio: Optional[str] = None
    prev_debt_equity_ratio: Optional[str] = None
    asset_allocation: Optional[Dict] = None
    yield_till_maturity: Decimal = Field(default=Decimal("0.000000"), decimal_places=6)
    maturity_date: Optional[date] = None
    modified_duration: Decimal = Field(default=Decimal("0.000000"), decimal_places=3)
    macaulay_duration: Decimal = Field(default=Decimal("0.000000"), decimal_places=3)
    aaa_sovereign_allocation: Decimal = Field(default=Decimal("0.000000"), decimal_places=6)
    holding_in_top_20_companies: Decimal = Field(default=Decimal("0.000000"), decimal_places=6)
    launch_date: Optional[date] = None
    close_date: Optional[date] = None
    allotment_date: Optional[date] = None
    sip_registration_start_date: Optional[date] = None
    sip_registration_end_date: Optional[date] = None
    w_score: Decimal = Field(default=Decimal("0.000000"), decimal_places=4)
    w_return_score: Decimal = Field(default=Decimal("0.000000"), decimal_places=4)
    w_risk_score: Decimal = Field(default=Decimal("0.000000"), decimal_places=4)
    w_valuation_score: Decimal = Field(default=Decimal("0.000000"), decimal_places=4)
    w_credit_quality_score: Decimal = Field(default=Decimal("0.000000"), decimal_places=4)
    ratings_as_on: Optional[date] = None
    wealthy_select: bool = False

    @field_validator('wschemecode')
    @classmethod
    def validate_wschemecode(cls, v):
        if not v:
            raise ValueError('wschemecode cannot be empty')
        return v

    @field_validator('wpc')
    @classmethod
    def validate_wpc(cls, v):
        if not v:
            raise ValueError('wpc cannot be empty')
        if not v.startswith('MF'):
            raise ValueError('wpc must start with MF')
        return v

class SchemeUpdate(BaseSettings):
    third_party_id: Optional[str] = None
    isin: Optional[str] = None
    isin_reinvestment: Optional[str] = None
    third_party_amc: Optional[str] = None
    class_code: Optional[str] = None
    amfi_code: Optional[str] = None
    scheme_code: Optional[str] = None
    scheme_code_ptm: Optional[str] = None
    scheme_code_dtm: Optional[str] = None
    tpsl_scheme_code: Optional[str] = None
    fund_family_code: Optional[str] = None
    scheme_name: Optional[str] = None
    benchmark: Optional[str] = None
    benchmark_tpid: Optional[str] = None
    display_name: Optional[str] = None
    category: Optional[str] = None
    scheme_type: Optional[SchemeType] = None
    aum: Optional[Decimal] = Field(None, decimal_places=4)
    lock_in_time: Optional[int] = None
    lock_in_unit: Optional[LockInUnitType] = None
    risk_o_meter_value: Optional[str] = None
    fund_manager: Optional[str] = None
    fund_manager_profile: Optional[str] = None
    objective: Optional[str] = None
    scheme_nature: Optional[SchemeNature] = None
    fund_type: Optional[MainCategory] = None
    amc: Optional[str] = None
    exit_load_time: Optional[int] = None
    exit_load_unit: Optional[ExitLoadUnitType] = None
    exit_load_percentage: Optional[Decimal] = Field(None, decimal_places=6)
    exit_load_remarks: Optional[str] = None
    latest_hnav_date: Optional[date] = None
    taxation_type: Optional[TaxationType] = None
    debt_equity_ratio: Optional[str] = None
    prev_debt_equity_ratio: Optional[str] = None
    asset_allocation: Optional[Dict] = None
    yield_till_maturity: Optional[Decimal] = Field(None, decimal_places=6)
    maturity_date: Optional[date] = None
    modified_duration: Optional[Decimal] = Field(None, decimal_places=3)
    macaulay_duration: Optional[Decimal] = Field(None, decimal_places=3)
    aaa_sovereign_allocation: Optional[Decimal] = Field(None, decimal_places=6)
    holding_in_top_20_companies: Optional[Decimal] = Field(None, decimal_places=6)
    launch_date: Optional[date] = None
    close_date: Optional[date] = None
    allotment_date: Optional[date] = None
    sip_registration_start_date: Optional[date] = None
    sip_registration_end_date: Optional[date] = None
    w_score: Optional[Decimal] = Field(None, decimal_places=4)
    w_return_score: Optional[Decimal] = Field(None, decimal_places=4)
    w_risk_score: Optional[Decimal] = Field(None, decimal_places=4)
    w_valuation_score: Optional[Decimal] = Field(None, decimal_places=4)
    w_credit_quality_score: Optional[Decimal] = Field(None, decimal_places=4)
    ratings_as_on: Optional[date] = None
    wealthy_select: Optional[bool] = None

class SchemeHoldingCreate(BaseSettings):
    wpc: str
    portfolio_date: Optional[date] = None
    holding_third_party_id: str
    holding_trading_symbol: Optional[str] = None
    holding_name: str
    holding_percentage: Decimal = Field(..., decimal_places=6)
    market_value: Decimal = Field(..., decimal_places=4)
    no_of_shares: int
    sector_name: str
    asset_type: str
    rating: str
    wrating: Optional[str] = None
    rating_agency: Optional[str] = None
    isin: Optional[str] = None
    reported_sector: Optional[str] = None

    @field_validator('wpc')
    @classmethod
    def validate_wpc(cls, v):
        if not v:
            raise ValueError('wpc cannot be empty')
        return v

    @field_validator('holding_third_party_id')
    @classmethod
    def validate_holding_third_party_id(cls, v):
        if not v:
            raise ValueError('holding_third_party_id cannot be empty')
        return v

# Add your CRUD operations here
