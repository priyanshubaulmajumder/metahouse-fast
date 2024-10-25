from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from decimal import Decimal
from datetime import date, datetime
from enum import Enum

class StockCategory(str, Enum):
    LARGE_CAP = 'L'
    MID_CAP = 'M'
    SMALL_CAP = 'S'

class StockBase(BaseModel):
    wstockcode: str = Field(..., max_length=28)
    wpc: Optional[str] = Field(None, max_length=12)
    third_party_id: str = Field(..., max_length=10)
    name: str = Field(..., max_length=256)
    bse_token: Optional[str] = Field(None, max_length=50)
    bse_symbol: Optional[str] = Field(None, max_length=50)
    nse_token: Optional[str] = Field(None, max_length=50)
    nse_symbol: Optional[str] = Field(None, max_length=50)
    nse_series: Optional[str] = Field(None, max_length=50)
    instrument_type: Optional[str] = Field(None, max_length=15)
    display_name: Optional[str] = Field(None, max_length=256)
    isin: Optional[str] = Field(None, max_length=20)
    sector: Optional[str] = Field(None, max_length=100)
    industry: Optional[str] = Field(None, max_length=100)
    category: Optional[StockCategory] = None

class StockResponse(StockBase):
    bse_lcp: Decimal
    bse_lcp_date: Optional[date]
    nse_lcp: Decimal
    nse_lcp_date: Optional[date]
    bse_latest_diff: Decimal
    nse_latest_diff: Decimal
    bse_latest_percentage_change: Decimal
    nse_latest_percentage_change: Decimal
    nse_hist_lcp_date: Optional[date]
    bse_hist_lcp_date: Optional[date]
    bse_52_week_high: Optional[Decimal]
    bse_52_week_low: Optional[Decimal]
    nse_52_week_high: Optional[Decimal]
    nse_52_week_low: Optional[Decimal]
    face_value: Decimal
    market_cap: Decimal
    no_of_shares: Decimal
    beta: Decimal
    w_take_buy: Decimal
    w_take_hold: Decimal
    w_take_sell: Decimal
    wealthy_score: Optional[int]
    hidden: bool
    is_listed: bool
    is_traded: bool
    image_url: Optional[str]
    deprecated_at: Optional[datetime]
    deprecate_reason: Optional[str]
    created_at: datetime
    updated_at: datetime
    current_ratio: Optional[Decimal]
    debt_to_equity: Optional[Decimal]
    rsi: Optional[Decimal]
    industry_pe_ratio: Optional[Decimal]
    macd: Optional[Decimal]
    ema: Optional[Decimal]
    sma: Optional[Decimal]
    std: Optional[Decimal]
    returns_one_month: Optional[Decimal]
    returns_three_months: Optional[Decimal]
    returns_six_months: Optional[Decimal]
    returns_one_year: Optional[Decimal]
    returns_two_years: Optional[Decimal]
    returns_three_years: Optional[Decimal]
    returns_five_years: Optional[Decimal]

    class Config:
        orm_mode = True

class TechnicalIndicatorsResponse(BaseModel):
    rsi: Optional[Decimal]
    macd: Optional[Decimal]
    ema: Optional[Decimal]
    sma: Optional[Decimal]
    std: Optional[Decimal]

class StockReturnsResponse(BaseModel):
    one_month: Optional[Decimal]
    three_months: Optional[Decimal]
    six_months: Optional[Decimal]
    one_year: Optional[Decimal]
    two_years: Optional[Decimal]
    three_years: Optional[Decimal]
    five_years: Optional[Decimal]

class PaginatedStockResponse(BaseModel):
    items: List[StockResponse]
    total: int
    skip: int
    limit: int

class StockHistPriceData(BaseModel):
    price_date: date
    open: Decimal
    close: Decimal
    low: Decimal
    high: Decimal
    volume: Decimal
    value: Decimal
    diff: Decimal
    percentage_change: Decimal

class StockFundamentalsResponse(BaseModel):
    pe: Optional[Decimal]
    pb: Optional[Decimal]
    dividend_yield: Optional[Decimal]
    dividend_payout: Optional[Decimal]
    eps: Optional[Decimal]
    book_value: Optional[Decimal]
    roa: Optional[Decimal]
    roe: Optional[Decimal]
    roce: Optional[Decimal]
    asset_turnover: Optional[Decimal]
    current_ratio: Optional[Decimal]
    debt_to_equity: Optional[Decimal]
    industry_pe_ratio: Optional[Decimal]

class ShareHoldingPatternResponse(BaseModel):
    promoters: Optional[Decimal]
    fii: Optional[Decimal]
    dii: Optional[Decimal]
    public: Optional[Decimal]
    others: Optional[Decimal]

class FinancialsOverviewResponse(BaseModel):
    revenue: Optional[Decimal]
    expenses: Optional[Decimal]
    profit_loss: Optional[Decimal]
    assets: Optional[Decimal]
    liabilities: Optional[Decimal]
    equity: Optional[Decimal]

class DetailedFinancialsResponse(BaseModel):
    balance_sheet: Dict[str, Decimal]
    profit_loss: Dict[str, Decimal]
    cash_flow: Dict[str, Decimal]

class StockManagementInfoResponse(BaseModel):
    director: Optional[dict]
    chairman_and_managing_director: Optional[str]
    address: Optional[str]
    telephone: Optional[str]
    fax_number: Optional[str]
    email: Optional[str]
    website: Optional[str]

class StockWCategoryMappingResponse(BaseModel):
    category: str
    exchange: str
    token: str
    name: str

    class Config:
        orm_mode = True

class StockCachedHPriceDataResponse(BaseModel):
    wstockcode: str
    third_party_id: str
    name: str
    latest_price_date: Optional[date]
    prices: Optional[Dict[str, Any]]

    class Config:
        orm_mode = True

class StockExchangeHistPriceDataResponse(BaseModel):
    id: int
    wstockcode: str
    price_date: date
    open: Decimal
    close: Decimal
    low: Decimal
    high: Decimal
    volume: Decimal
    value: Decimal
    diff: Decimal
    percentage_change: Decimal

    class Config:
        orm_mode = True

class StockIDWPCMappingResponse(BaseModel):
    id: str
    identifier: str
    wpc: str
    wstockcode: str
    identifier_type: str

    class Config:
        orm_mode = True

class StockHistPriceDataResponse(BaseModel):
    id: int
    wstockcode: str
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int
    exchange: str

    class Config:
        orm_mode = True

class TechnicalIndicatorsResponse(BaseModel):
    rsi: Optional[Decimal]
    macd: Optional[Decimal]
    ema: Optional[Decimal]
    sma: Optional[Decimal]
    std: Optional[Decimal]

class StockReturnsResponse(BaseModel):
    one_month: Optional[Decimal]
    three_months: Optional[Decimal]
    six_months: Optional[Decimal]
    one_year: Optional[Decimal]
    two_years: Optional[Decimal]
    three_years: Optional[Decimal]
    five_years: Optional[Decimal]

class StockHistPriceDataBase(BaseModel):
    wstockcode: str
    price_date: date
    open: Decimal
    close: Decimal
    low: Decimal
    high: Decimal
    volume: Decimal
    value: Decimal
    diff: Decimal
    percentage_change: Decimal

class StockBSEHistPriceData(StockHistPriceDataBase):
    id: int

    class Config:
        orm_mode = True

class StockNSEHistPriceData(StockHistPriceDataBase):
    id: int

    class Config:
        orm_mode = True
