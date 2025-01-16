from sqlalchemy import Column, Float, String, Boolean, Numeric, Date, DateTime, ForeignKey, Index, Integer, Text, Enum as modelEnum, JSON, UniqueConstraint, event
from sqlalchemy.orm import relationship, object_session
from sqlalchemy.sql import func
from app.db.base import Base
from app.utils.model_utils import WealthyProductCodeField, WealthyExternalIdField, generate_wealthy_stock_code
from decimal import Decimal
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum as Enum
from app.models.base import BaseModel
from app.utils.constants import StockCategory, WResultType, WResultPeriod
from sqlmodel import Field, SQLModel, Enum, Index, UniqueConstraint
from sqlalchemy.sql import func
from decimal import Decimal
from datetime import date, datetime
from enum import Enum as PyEnum
from app.models.base import BaseModel
from app.utils.constants import WResultPeriod
from enum import Enum
from typing import Optional

class StockCategory(str, Enum):
    LARGE_CAP = 'L'
    MID_CAP = 'M'
    SMALL_CAP = 'S'



class StockIDGenerator(BaseModel, table=True):
    __tablename__ = "funnal_stockidgenerator"
    generated_id: int = Field( primary_key= True)
    # Add new fields or methods if needed

class Stock(BaseModel, table=True):
    __tablename__ = "funnal_stock"

    wstockcode: str = Field(max_length=28,primary_key= True)
    wpc: str = WealthyProductCodeField(prefix="ST", Modal=StockIDGenerator, max_length=12, null=True, blank=True)
    third_party_id: str = Field(default=None, max_length=10)
    name: str = Field(default=None, max_length=256)
    bse_token: str = Field(default=None, max_length=50, nullable=True)
    bse_symbol: str = Field(default=None, max_length=50, nullable=True)
    nse_token: str = Field(default=None, max_length=50, nullable=True)
    nse_symbol: str = Field(default=None, max_length=50, nullable=True)
    nse_series: str = Field(default=None, max_length=50, nullable=True)
    instrument_type: str = Field(default=None, max_length=15, nullable=True)
    display_name: str = Field(default=None, max_length=256, nullable=True)
    isin: str = Field(default=None, max_length=20, nullable=True)
    sector: str = Field(default=None, max_length=100, nullable=True)
    industry: str = Field(default=None, max_length=100, nullable=True)
    category: Optional[StockCategory] = Field(default=None, nullable=True)
    
    bse_lcp: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    bse_lcp_date: date = Field(default=None, nullable=True)
    nse_lcp: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    nse_lcp_date: date = Field(default=None, nullable=True)
    bse_latest_diff: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    nse_latest_diff: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    bse_latest_percentage_change: Decimal = Field(default=Decimal("0.000"), max_digits=7, decimal_places=3)
    nse_latest_percentage_change: Decimal = Field(default=Decimal("0.000"), max_digits=7, decimal_places=3)
    nse_hist_lcp_date: date = Field(default=None, nullable=True)
    bse_hist_lcp_date: date = Field(default=None, nullable=True)
    
    bse_52_week_high: Decimal = Field(default=None, max_digits=20, decimal_places=3)
    bse_52_week_low: Decimal = Field(default=None, max_digits=20, decimal_places=3)
    nse_52_week_high: Decimal = Field(default=None, max_digits=20, decimal_places=3)
    nse_52_week_low: Decimal = Field(default=None, max_digits=20, decimal_places=3)
    
    face_value: Decimal = Field(default=Decimal("0.000"), max_digits=5, decimal_places=3)
    market_cap: Decimal = Field(default=Decimal("0.000"), max_digits=30, decimal_places=3)
    no_of_shares: Decimal = Field(default=Decimal("0.0"), max_digits=15, decimal_places=1)
    
    beta: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    pe: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    pb: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    dividend_yield: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)
    dividend_payout: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    eps: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    book_value: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    roa: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)
    roe: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)
    roce: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)
    asset_turnover: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)
    current_ratio: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)
    debt_to_equity: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)
    
    rsi: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    industry_pe_ratio: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    macd: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    ema: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    sma: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    std: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    
    returns_ytd: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    returns_one_week: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    returns_one_month: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    returns_three_months: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    returns_six_months: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    returns_one_year: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    returns_two_years: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    returns_two_years_cagr: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    returns_three_years: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    returns_three_years_cagr: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    returns_five_years: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    returns_five_years_cagr: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    
    # cashflow, quarterly, yearly
    # missing API for this
    # prefix it with cf_, have to remove these fields but not removing until a separate schema for the same is finalised
    operating_activities: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    investing_activities: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    financing_activities: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    others_activities: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    net_cash_flow: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    # missing API for this
    
    w_take_buy: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    w_take_hold: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    w_take_sell: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    wealthy_score: int = Field(default=None, nullable=True)
    hidden: bool = Field(default=False)
    is_listed: bool = Field(default=False)
    is_traded: bool = Field(default=False)
    deprecated_at: datetime = Field(default=None, nullable=True)
    deprecate_reason: str = Field(default=None, max_length=254, nullable=True)
    
    __table_args__ = (
        Index('ix_stock_thid_party_id_1', 'third_party_id'),
        Index('ix_stock_isin_1', 'isin'),
        Index('ix_stock_bse_token_11', 'bse_token'),
        Index('ix_stock_nse_token_12', 'nse_token'),
        Index('ix_stock_wpc_13', 'wpc'),
        Index('ix_stock_bse_symbol_14', 'bse_symbol'),
        Index('ix_stock_nse_symbol_15', 'nse_symbol'),
    )

    @property
    def image_url(self):
        if not self.isin:
            return None
        return f"https://broking-public.s3.ap-south-1.amazonaws.com/stocks/{self.isin}.png"
    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     if not self.pk:
    #         from funnal.tasks import update_mappings_for_stock
    #         update_mappings_for_stock(wpc=self.wpc)
    #     if self.sector:
    #         self.sector = str(self.sector).upper()
    #     if self.isin:
    #         self.isin = str(self.isin).upper()
    #     if self.nse_token:
    #         self.nse_token = str(self.nse_token).upper()
    #     if self.bse_token:
    #         self.bse_token = str(self.bse_token).upper()
    #     if self.nse_symbol:
    #         self.nse_symbol = str(self.nse_symbol).upper()
    #     if self.bse_symbol:
    #         self.bse_symbol = str(self.bse_symbol).upper()
    #     if self.third_party_id:
    #         self.third_party_id = str(self.third_party_id).upper()
    #     if not self.wstockcode:
    #         self.wstockcode = generate_wealthy_stock_code(self)
    #     return super(Stock, self).save(
    #         force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields
    #     )

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True

class StockNSEHistPriceData(BaseModel, table=True):
    __tablename__ = "funnal_stocknsehistpricedata"
    id: int = Field(primary_key=True)
    wstockcode: str = Field(default=None, max_length=28)
    price_date: date = Field(default=None)
    open: Decimal = Field(default=Decimal('0.000000'), max_digits=20, decimal_places=6)
    close: Decimal = Field(default=Decimal('0.000000'), max_digits=20, decimal_places=6)
    low: Decimal = Field(default=Decimal('0.000000'), max_digits=20, decimal_places=6)
    high: Decimal = Field(default=Decimal('0.000000'), max_digits=20, decimal_places=6)
    volume: Decimal = Field(default=Decimal('0.000000'), max_digits=20, decimal_places=6)
    value: Decimal = Field(default=Decimal('0.000000'), max_digits=20, decimal_places=6)
    diff: Decimal = Field(default=Decimal('0.000000'), max_digits=20, decimal_places=6)
    percentage_change: Decimal = Field(default=Decimal('0.000000'), max_digits=20, decimal_places=6)
    
    __table_args__ = (
        Index('ix_snsehp_wstockcode_1', 'wstockcode'),
        UniqueConstraint('wstockcode', 'price_date', name='uq_snsehp_wstockcode_price_date'),
    )

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
class StockBSEHistPriceData(BaseModel, table=True):
    __tablename__ = "funnal_stockbsehistpricedata"
    id: int = Field(primary_key=True)
    wstockcode: str = Field(default=None, max_length=28)
    price_date: date = Field(default=None)
    open: Decimal = Field(default=Decimal('0.000000'), max_digits=20, decimal_places=6)
    close: Decimal = Field(default=Decimal('0.000000'), max_digits=20, decimal_places=6)
    low: Decimal = Field(default=Decimal('0.000000'), max_digits=20, decimal_places=6)
    high: Decimal = Field(default=Decimal('0.000000'), max_digits=20, decimal_places=6)
    volume: Decimal = Field(default=Decimal('0.000000'), max_digits=20, decimal_places=6)
    value: Decimal = Field(default=Decimal('0.000000'), max_digits=20, decimal_places=6)
    diff: Decimal = Field(default=Decimal('0.000000'), max_digits=20, decimal_places=6)
    percentage_change: Decimal = Field(default=Decimal('0.000000'), max_digits=20, decimal_places=6)
    
    __table_args__ = (
        Index('ix_sbsehp_wstockcode_1', 'wstockcode'),
        UniqueConstraint('wstockcode', 'price_date', name='uq_sbsehp_wstockcode_price_date'),
    )
    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
        
class StockManagementInfo(BaseModel, table=True):
    __tablename__ = "funnal_stockmanagementinfo"
    id: int = Field(primary_key=True)
    wstockcode: str = Field(default=None, max_length=28)
    director: dict = Field(sa_column=Column(JSONB))
    chairman_and_managing_director: str = Field(default=None, max_length=50, nullable=True)
    address: str = Field(default=None, nullable=True)
    telephone: str = Field(default=None, max_length=18, nullable=True)
    fax_number: str = Field(default=None, max_length=12, nullable=True)
    email: str = Field(default=None, max_length=254, nullable=True)
    website: str = Field(default=None, max_length=50, nullable=True)


    __table_args__ = (
        Index('ix_smi_wstockcode_11', 'wstockcode'),
    )
    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True 
class StockWCategoryMapping(BaseModel, table=True):
    __tablename__ = "funnal_stockwcategorymapping"
    id: int = Field(primary_key=True)
    category: str = Field(default=None, max_length=10)
    exchange: str = Field(default="nse", max_length=4)
    token: str = Field( max_length=10)
    name: str = Field(default=None, max_length=256)
    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
class StockIDWPCMapping(BaseModel, table=True):
    __tablename__ = "funnal_stockidwpcmapping"
    id: int = Field(primary_key=True)
    identifier: str = Field(default=None, max_length=50, nullable=False)
    wpc: str = Field(default=None, max_length=12, nullable=False)
    wstockcode: str = Field(default=None, max_length=28, nullable=False)
    identifier_type: str = Field(default=None, max_length=15, nullable=False)

    __table_args__ = (
        UniqueConstraint('identifier', 'wpc', name='uq_identifier_wpc'),
        Index('ix_siwm_identifier_909', 'identifier'),
        Index('ix_siwm_idtype_397', 'identifier_type'),
    )
    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True

class StockYearlyRatioHistData(BaseModel, table=True):
    __tablename__ = "funnal_stockyearlyratiohistdata"
    id: int = Field(primary_key=True)
    wstockcode: str = Field(nullable=False, max_length=28)
    ratio_date: date = Field(nullable=False)
    pe: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    pb: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    dividend_yield: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)
    eps: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    book_value: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    roa: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)
    roe: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)
    roce: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)
    asset_turnover: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)
    current_ratio: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)
    debt_to_equity: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)

    __table_args__ = (
        Index('ix_syrhd_wstockcode', 'wstockcode'),
        UniqueConstraint('wstockcode', 'ratio_date', name='uq_syrhd_wstockcode_ratio_date'),
    )

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True

class StockShareHoldingHistData(BaseModel, table=True):
    __tablename__ = "funnal_stockshareholdinghistdata"
    id: int = Field(primary_key=True)
    wstockcode: str = Field(nullable=False, max_length=28)
    holding_date: date = Field(nullable=False)
    promoter_holding: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)
    fpi_holding: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)
    dii_holding: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)
    others_holding: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3)

    __table_args__ = (
        Index('ix_sshhd_wstockcode', 'wstockcode'),
        UniqueConstraint('wstockcode', 'holding_date', name='uq_sshhd_wstockcode_holding_date'),
    )

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True

class StockBonusHistData(BaseModel, table=True):
    __tablename__ = "funnal_stockbonushistdata"
    id: int = Field(primary_key=True)
    wstockcode: str = Field(nullable=False, max_length=28)
    announce_date: date = Field(nullable=True)
    ex_bonus_date: date = Field(nullable=True)
    record_date: date = Field(nullable=True)
    bonus_ratio: str = Field(nullable=True, max_length=20)
    bonus_type: str = Field(nullable=True, max_length=20)
    remarks: str = Field(nullable=True)

    __table_args__ = (
        Index('ix_sbh_wstockcode', 'wstockcode'),
    )

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True

# This class represents historical data for stock splits, including details such as stock code,
# announcement date, split ratio, and face value.
# class StockSplitHistData(BaseModel, table=True):
#     __tablename__ = "funnal_stocksplithistdata"

#     id: int = Field()
#     wstockcode: str = Field(nullable=False, max_length=28)
#     announce_date: date = Field(nullable=True)
#     ex_split_date: date = Field(nullable=True)
#     record_date: date = Field(nullable=True)
#     split_ratio: str = Field(nullable=True, max_length=20)
#     face_value: Decimal = Field(max_digits=10, decimal_places=3)
#     remarks: str = Field(nullable=True)

#     __table_args__ = (
#         Index('ix_ssh_wstockcode', 'wstockcode'),
#     )

#     class Config:
#         arbitrary_types_allowed = True
#         use_enum_values = True

class StockRightsHistData(BaseModel, table=True):
    __tablename__ = "funnal_stockrightshistdata"
    id: int = Field(primary_key=True)
    wstockcode: str = Field(nullable=False, max_length=28)
    announce_date: date = Field(nullable=True)
    ex_rights_date: date = Field(nullable=True)
    record_date: date = Field(nullable=True)
    rights_ratio: str = Field(nullable=True, max_length=20)
    issue_price: Decimal = Field(nullable=True, max_digits=20, decimal_places=3)
    premium: Decimal = Field(nullable=True, max_digits=20, decimal_places=3)
    remarks: str = Field(nullable=True)

    __table_args__ = (
        Index('ix_srh_wstockcode', 'wstockcode'),
    )

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True

class StockBoardMeetingHistData(BaseModel, table=True):
    __tablename__ = "funnal_stockboardmeetinghistdata"
    id: int = Field(primary_key=True)
    wstockcode: str = Field(nullable=False, max_length=28)
    meeting_date: date = Field(nullable=True)
    purpose: str = Field(nullable=True)
    outcome: str = Field(nullable=True)
    remarks: str = Field(nullable=True)

    __table_args__ = (
        Index('ix_sbmhd_wstockcode', 'wstockcode'),
    )

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True

class ResultType(PyEnum):
    Standalone = 'S'
    Consolidated = 'C'

class StockFinancialQuarterlyResult(BaseModel, table=True):
    __tablename__ = "funnal_stockfinancialquarterlyresult"

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
        table_args = {'extend_existing': True}
    id: int = Field(primary_key=True)
    wstockcode: str = Field(max_length=28, nullable=False)
    rtype: ResultType = Field(nullable=False)
    year: int = Field(nullable=True)
    month: int = Field(nullable=True)
    net_sales: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    other_operating_income: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    other_income: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    total_income: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    total_expenditure: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    interest: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    ebitda: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    ebit: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    ebt: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    depreciation: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    tax: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    net_profit: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    extra_ordinary_items: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    adj_profit_after_extra_ordinary_items: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    eps: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    eps_adj: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    book_value: Decimal = Field(default=Decimal("0.000"), max_digits=7, decimal_places=3, nullable=True)
    diluted_eps: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    dividend_per_share: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    patm_pct: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3, nullable=True)
    equity: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)


    __table_args__ = (
        Index('ix_sfqr_wstockcode', 'wstockcode'),
    )
    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
class StockFinancialHalfYearlyResult(BaseModel, table=True):
    __tablename__ = "funnal_stockfinancialhalfyearlyresult"
    id: int = Field(primary_key=True)
    wstockcode: str = Field(max_length=28, nullable=False)
    rtype: ResultType = Field(nullable=False)
    year: int = Field(nullable=True)
    month: int = Field(nullable=True)
    net_sales: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    other_operating_income: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    other_income: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    total_income: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    total_expenditure: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    interest: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    ebitda: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    ebit: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    ebt: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    depreciation: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    tax: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    net_profit: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    extra_ordinary_items: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    adj_profit_after_extra_ordinary_items: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    eps: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    eps_adj: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    book_value: Decimal = Field(default=Decimal("0.000"), max_digits=7, decimal_places=3, nullable=True)
    diluted_eps: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    dividend_per_share: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    patm_pct: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3, nullable=True)
    equity: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)

    __table_args__ = (
        Index('ix_sfhyr_wstockcode', 'wstockcode'),
    )

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True

class StockFinancialNineMonthResult(BaseModel, table=True):
    __tablename__ = "funnal_stockfinancialninemonthresult"
    id: int = Field(primary_key=True)
    wstockcode: str = Field(max_length=28, nullable=False)
    rtype: ResultType = Field(nullable=False)
    year: int = Field(nullable=True)
    month: int = Field(nullable=True)
    net_sales: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    other_operating_income: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    other_income: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    total_income: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    total_expenditure: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    interest: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    ebitda: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    ebit: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    ebt: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    depreciation: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    tax: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    net_profit: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    extra_ordinary_items: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    adj_profit_after_extra_ordinary_items: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    eps: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    eps_adj: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    book_value: Decimal = Field(default=Decimal("0.000"), max_digits=7, decimal_places=3, nullable=True)
    diluted_eps: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    dividend_per_share: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    patm_pct: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3, nullable=True)
    equity: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)

    __table_args__ = (
        Index('ix_sfnmr_wstockcode', 'wstockcode'),
    )

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True

class StockFinancialYearlyResult(BaseModel, table=True):
    __tablename__ = "funnal_stockfinancialyearlyresult"

    id: int = Field(primary_key=True)
    wstockcode: str = Field(max_length=28, nullable=False)
    rtype: ResultType = Field(nullable=False)
    year: int = Field(nullable=True)
    month: int = Field(nullable=True)
    net_sales: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    other_operating_income: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    other_income: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    total_income: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    total_expenditure: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    interest: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    ebitda: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    ebit: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    ebt: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    depreciation: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    tax: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    net_profit: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    extra_ordinary_items: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    adj_profit_after_extra_ordinary_items: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    eps: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    eps_adj: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    book_value: Decimal = Field(default=Decimal("0.000"), max_digits=7, decimal_places=3, nullable=True)
    diluted_eps: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    dividend_per_share: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)
    patm_pct: Decimal = Field(default=Decimal("0.000"), max_digits=10, decimal_places=3, nullable=True)
    equity: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3, nullable=True)

    __table_args__ = (
        Index('ix_sfyr_wstockcode', 'wstockcode'),
    )

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True

result_period_model_mapping = {
    WResultPeriod.Quarterly: StockFinancialQuarterlyResult,
    WResultPeriod.HalfYearly: StockFinancialHalfYearlyResult,
    WResultPeriod.NineMonth: StockFinancialNineMonthResult,
    WResultPeriod.Yearly: StockFinancialYearlyResult,
}


# Financials End



# https://wealthyapis.cmots.com/api/ResultBalancesheetQuarterly/476/S
class StockBalanceSheetQuarterly(BaseModel, table=True):
    __tablename__ = "funnal_stockbalancesheetquarterly"
    id: int = Field(primary_key=True)
    wstockcode: str = Field(default=None, max_length=28, nullable=False)
    rtype: WResultType = Field(default=None, nullable=False)
    # equities and liabilities
    share_capital: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    reserves_and_surplus: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    current_liabilities: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    other_liabilities: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    total_liabilities: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    contingent_liabilities: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)

    # assets
    fixed_assets: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    current_assets: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    other_assets: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    total_assets: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)

    # profit and loss, quarterly, yearly
    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True


# https://wealthyapis.cmots.com/api/ResultBalancesheetHalfyearly/476/S
class StockBalanceSheet(BaseModel, table=True):
    __tablename__ = "funnal_stockbalancesheet"
    id: int = Field(primary_key=True)
    wstockcode: str = Field(default=None, max_length=28, nullable=False)
    rtype: WResultType = Field(default=None, nullable=False)

    # equities and liabilities
    share_capital: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    reserves_and_surplus: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    current_liabilities: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    other_liabilities: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    total_liabilities: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    contingent_liabilities: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)

    # assets
    fixed_assets: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    current_assets: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    other_assets: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    total_assets: Decimal = Field(default=Decimal("0.000"), max_digits=20, decimal_places=3)
    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
    # profit and loss, quarterly, yearly



#Financial Ends


# Balance Sheet Start

# option available are /s and /c, s: standalone and c: consolidated
# https://wealthyapis.cmots.com/api/Balancesheet/6/s
# https://wealthyapis.cmots.com/api/ResultBalancesheetyearly/476/S

# Balance Sheet End

