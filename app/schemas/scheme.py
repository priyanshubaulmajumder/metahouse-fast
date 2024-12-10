from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, validator, BaseModel
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from decimal import Decimal
from enum import Enum

class SchemeType(str, Enum):
    OPEN_ENDED = 'OE'
    CLOSE_ENDED = 'CE'
    INTERVAL = 'IN'

class LockInUnitType(str, Enum):
    Days = 'D'
    Months = 'M'
    Years = 'Y'

class SchemeNatureEnum(str, Enum):
    Open = 'Open'
    Close = 'Close'
    Interval = 'Interval'
    
class MainCategory(str, Enum):
    Equity = 'E'
    Debt = 'D'
    Hybrid = 'H'
    Other = 'O'

class ExitLoadUnitType(str, Enum):
    Days = 'D'
    Months = 'M'
    Years = 'Y'

class TaxationType(str, Enum):
    Equity = 'E'
    Debt = 'D'

class SchemeIdType(str, Enum):
    WSchemeCode = 'wschemecode'
    ISIN = 'isin'
    WPC = 'wpc'
    SchemeCode = 'scheme-code'
    TPID = 'tp-id'
    ThirdPartyId = 'third-party-id'

class ResolveResultSchema(BaseSettings):
    resolved: Dict[str, Any] = {}
    resolved_new_wpcs: Dict[str, Any] = {}
    unresolved: List[str] = []
    
class SchemeIDGenerator(BaseSettings):
    generated_id: int
    class Config:
        from_attributes = True
        
class SchemeHistNavDataSchema(BaseModel):
    
    wpc: str
    nav_date: date  
    nav: float
    adj_nav: float
    diff: float
    percentage_change: float
    class Config:
        from_attributes = True

class WPCToTWPCMapping(BaseSettings):
    external_id: str
    wpc: str
    target_wpc: str
    hidden: bool
    class Config:
        from_attributes = True


class SectorToWSectorMapping(BaseSettings):
    external_id: str
    sector: str
    wsector: str
    class Config:
        from_attributes = True


class SchemeHolding(BaseSettings):
    scheme_id: int
    holding_id: int
    holding_percentage: float
    class Config:
        from_attributes = True


class WSchemeCodeWPCMapping(BaseSettings):
    wscheme_code: str
    wpc: str
    class Config:
        from_attributes = True


class SchemeCodeWPCMapping(BaseSettings):
    scheme_code: str
    wpc: str
    class Config:
        from_attributes = True


class WPCWPCMapping(BaseSettings):
    wpc: str
    target_wpc: str
    class Config:
        from_attributes = True


class ParentChildSchemeMapping(BaseSettings):
    parent_scheme_id: int
    child_scheme_id: int
    class Config:
        from_attributes = True


class SchemeAudit(BaseSettings):
    scheme_id: int
    audit_date: datetime
    audit_result: str
    class Config:
        from_attributes = True


class SchemeNature(BaseSettings):
    nature: SchemeNatureEnum
    class Config:
        from_attributes = True


class Scheme(BaseSettings):
    id: int
    name: str
    third_party_id: str
    isin: Optional[str]
    amfi_code: Optional[str]
    scheme_code: Optional[str]
    wschemecode: Optional[str]
    deprecate_reason: Optional[str]
    w_rating: float
    w_score: float
    w_return_score: float
    w_risk_score: float
    w_valuation_score: float
    w_credit_quality_score: float
    ratings_as_on: Optional[datetime]
    wealthy_select: bool

    @validator('third_party_id')
    def validate_third_party_id(cls, v):
        if not v:
            raise ValueError('third_party_id cannot be empty')
        return v
    class Config:
        from_attributes = True


class SchemeUniqueIDsCacheService(BaseSettings):
    cache_key: str
    cache_value: str
    class Config:
        from_attributes = True


class SchemeResponse(Scheme):
    pass

class SchemeSerializer(BaseSettings):
    wschemecode: str
    wpc: str
    third_party_id: Optional[str]
    isin: Optional[str]
    isin_reinvestment: Optional[str]
    third_party_amc: Optional[str]
    class_code: Optional[str]
    amfi_code: Optional[str]
    scheme_code: Optional[str]
    scheme_code_ptm: Optional[str]
    scheme_code_dtm: Optional[str]
    tpsl_scheme_code: Optional[str]
    fund_family_code: Optional[str]
    scheme_name: Optional[str]
    benchmark: Optional[str]
    benchmark_tpid: Optional[str]
    display_name: Optional[str]
    category: Optional[str]
    scheme_type: Optional[SchemeType]
    aum: Optional[Decimal] = Field(None, decimal_places=4)
    lock_in_time: Optional[int]
    lock_in_unit: LockInUnitType = LockInUnitType.Years
    risk_o_meter_value: Optional[str]
    fund_manager: Optional[str]
    fund_manager_profile: Optional[str]
    objective: Optional[str]
    scheme_nature: SchemeNatureEnum = SchemeNatureEnum.Open
    fund_type: MainCategory = MainCategory.Equity
    amc: Optional[str]
    exit_load_time: Optional[int]
    exit_load_unit: ExitLoadUnitType = ExitLoadUnitType.Years
    exit_load_percentage: Optional[Decimal] = Field(None, decimal_places=6)
    exit_load_remarks: Optional[str]
    latest_hnav_date: Optional[date]
    taxation_type: Optional[TaxationType]
    debt_equity_ratio: Optional[str]
    prev_debt_equity_ratio: Optional[str]
    asset_allocation: Optional[Dict]
    yield_till_maturity: Decimal = Field(default=Decimal("0.000000"), decimal_places=6)
    maturity_date: Optional[date]
    modified_duration: Decimal = Field(default=Decimal("0.000000"), decimal_places=3)
    macaulay_duration: Decimal = Field(default=Decimal("0.000000"), decimal_places=3)
    aaa_sovereign_allocation: Decimal = Field(default=Decimal("0.000000"), decimal_places=6)
    holding_in_top_20_companies: Decimal = Field(default=Decimal("0.000000"), decimal_places=6)
    launch_date: Optional[date]
    close_date: Optional[date]
    allotment_date: Optional[date]
    sip_registration_start_date: Optional[date]
    sip_registration_end_date: Optional[date]
    w_score: Decimal = Field(default=Decimal("0.000000"), decimal_places=4)
    w_return_score: Decimal = Field(default=Decimal("0.000000"), decimal_places=4)
    w_risk_score: Decimal = Field(default=Decimal("0.000000"), decimal_places=4)
    w_valuation_score: Decimal = Field(default=Decimal("0.000000"), decimal_places=4)
    w_credit_quality_score: Decimal = Field(default=Decimal("0.000000"), decimal_places=4)
    ratings_as_on: Optional[date]
    wealthy_select: bool = False
    created_at: datetime
    updated_at: datetime
    scheme_nature: SchemeNatureEnum = SchemeNatureEnum.Open
    class Config:
        from_attributes = True

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

    @property
    def is_tax_saver(self):
        if not self.category:
            return False
        return "elss" in str(self.category).lower()

    @property
    def is_payment_allowed(self):
        if self.close_date and self.sip_registration_start_date:
            now = date.today()
            if self.close_date <= now <= self.sip_registration_start_date:
                return False
        return True

    @property
    def dynamic_payment_blocked_reason(self):
        if self.close_date and self.sip_registration_start_date:
            now = date.today()
            if self.close_date <= now <= self.sip_registration_start_date:
                return 'Investment is currently not allowed in this NFO'
        return None

class SchemeHoldingSerializer(BaseSettings):
    external_id: str
    wpc: str
    portfolio_date: Optional[date]
    holding_third_party_id: str
    holding_trading_symbol: Optional[str]
    holding_name: str
    holding_percentage: Decimal = Field(..., decimal_places=6)
    market_value: Decimal = Field(..., decimal_places=4)
    no_of_shares: int
    sector_name: str
    asset_type: str
    rating: str
    wrating: Optional[str]
    rating_agency: Optional[str]
    isin: Optional[str]
    reported_sector: Optional[str]

    class Config:
        from_attributes = True

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

SchemeResponse = SchemeSerializer


class InvestmentTypeChoices:
    ONETIME = "onetime"
    SIP = "sip"
    

class ReturnsRequest(BaseModel):
    id_type: str
    id_value: str
    amount: int = Field(gt=0)
    period: int = Field(gt=0, alias='n_years')
    investment_type: str
    sip_day: Optional[int] = Field(default=None, ge=1, le=28)
    
    
class ReturnsData(BaseModel):
    invested_value: Optional[float]
    current_value: Optional[float]
    xirr: Optional[float]
    xirr_percentage: Optional[float]
    absolute_returns: Optional[float]
    absolute_returns_percentage: Optional[float]
    returns_details: List[SchemeHistNavDataSchema]