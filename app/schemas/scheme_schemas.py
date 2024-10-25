from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict
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

class SchemeNature(str, Enum):
    Open = 'O'
    Close = 'C'

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

class SchemeSerializer(BaseModel):
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
    scheme_nature: SchemeNature = SchemeNature.Open
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

    class Config:
        orm_mode = True

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

class SchemeHoldingSerializer(BaseModel):
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
        orm_mode = True

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




class SchemeResponse(SchemeSerializer):
    pass 
