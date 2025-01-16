from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional, Dict, Any
from decimal import Decimal
from datetime import date, datetime
from enum import Enum
from app.utils.constants import StockCategory, WResultType, WResultPeriod
from pydantic import BaseModel
from enum import Enum as PyEnum

class StockCategory(PyEnum):
    LARGE_CAP = 'L'
    MID_CAP = 'M'
    SMALL_CAP = 'S'

class StockIDGeneratorSchema(BaseModel):
    generated_id: int

class StockSchema(BaseModel):
    wstockcode: str
    wpc: Optional[str]
    third_party_id: Optional[str]
    name: Optional[str]
    bse_token: Optional[str]
    bse_symbol: Optional[str]
    nse_token: Optional[str]
    nse_symbol: Optional[str]
    nse_series: Optional[str]
    instrument_type: Optional[str]
    display_name: Optional[str]
    isin: Optional[str]
    sector: Optional[str]
    industry: Optional[str]
    category: Optional[StockCategory]
    bse_lcp: Optional[Decimal] = Decimal("0.000")
    bse_lcp_date: Optional[date]
    nse_lcp: Optional[Decimal] = Decimal("0.000")
    nse_lcp_date: Optional[date]
    bse_latest_diff: Optional[Decimal] = Decimal("0.000")
    nse_latest_diff: Optional[Decimal] = Decimal("0.000")
    bse_latest_percentage_change: Optional[Decimal] = Decimal("0.000")
    nse_latest_percentage_change: Optional[Decimal] = Decimal("0.000")
    nse_hist_lcp_date: Optional[date]
    bse_hist_lcp_date: Optional[date]
    bse_52_week_high: Optional[Decimal]
    bse_52_week_low: Optional[Decimal]
    nse_52_week_high: Optional[Decimal]
    nse_52_week_low: Optional[Decimal]
    face_value: Optional[Decimal] = Decimal("0.000")
    market_cap: Optional[Decimal] = Decimal("0.000")
    no_of_shares: Optional[Decimal] = Decimal("0.0")
    beta: Optional[Decimal] = Decimal("0.000")
    ratios_as_on: Optional[date]
    pe: Optional[Decimal] = Decimal("0.000")
    pb: Optional[Decimal] = Decimal("0.000")
    dividend_yield: Optional[Decimal] = Decimal("0.000")
    dividend_payout: Optional[Decimal] = Decimal("0.000")
    eps: Optional[Decimal] = Decimal("0.000")
    book_value: Optional[Decimal] = Decimal("0.000")
    roa: Optional[Decimal] = Decimal("0.000")
    roe: Optional[Decimal] = Decimal("0.000")
    roce: Optional[Decimal] = Decimal("0.000")
    asset_turnover: Optional[Decimal] = Decimal("0.000")
    current_ratio: Optional[Decimal] = Decimal("0.000")
    debt_to_equity: Optional[Decimal] = Decimal("0.000")
    rsi: Optional[Decimal] = Decimal("0.000")
    industry_pe_ratio: Optional[Decimal] = Decimal("0.000")
    macd: Optional[Decimal] = Decimal("0.000")
    ema: Optional[Decimal] = Decimal("0.000")
    sma: Optional[Decimal] = Decimal("0.000")
    std: Optional[Decimal] = Decimal("0.000")
    returns_ytd: Optional[Decimal] = Decimal("0.000")
    returns_one_week: Optional[Decimal] = Decimal("0.000")
    returns_one_month: Optional[Decimal] = Decimal("0.000")
    returns_three_months: Optional[Decimal] = Decimal("0.000")
    returns_six_months: Optional[Decimal] = Decimal("0.000")
    returns_one_year: Optional[Decimal] = Decimal("0.000")
    returns_two_years: Optional[Decimal] = Decimal("0.000")
    returns_two_years_cagr: Optional[Decimal] = Decimal("0.000")
    returns_three_years: Optional[Decimal] = Decimal("0.000")
    returns_three_years_cagr: Optional[Decimal] = Decimal("0.000")
    returns_five_years: Optional[Decimal] = Decimal("0.000")
    returns_five_years_cagr: Optional[Decimal] = Decimal("0.000")
    w_take_buy: Optional[Decimal] = Decimal("0.000")
    w_take_hold: Optional[Decimal] = Decimal("0.000")
    w_take_sell: Optional[Decimal] = Decimal("0.000")
    wealthy_score: Optional[int]
    hidden: Optional[bool] = False
    is_listed: Optional[bool] = False
    is_traded: Optional[bool] = False
    deprecated_at: Optional[datetime]
    deprecate_reason: Optional[str]


class StockBase(BaseSettings):
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

class TechnicalIndicatorsResponse(BaseSettings):
    rsi: Optional[Decimal]
    macd: Optional[Decimal]
    ema: Optional[Decimal]
    sma: Optional[Decimal]
    std: Optional[Decimal]

class StockReturnsResponse(BaseSettings):
    one_month: Optional[Decimal]
    three_months: Optional[Decimal]
    six_months: Optional[Decimal]
    one_year: Optional[Decimal]
    two_years: Optional[Decimal]
    three_years: Optional[Decimal]
    five_years: Optional[Decimal]

class PaginatedStockResponse(BaseSettings):
    items: List[StockResponse]
    total: int
    skip: int
    limit: int

class StockHistPriceData(BaseSettings):
    price_date: date
    open: Decimal
    close: Decimal
    low: Decimal
    high: Decimal
    volume: Decimal
    value: Decimal
    diff: Decimal
    percentage_change: Decimal

class StockFundamentalsResponse(BaseSettings):
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

class ShareHoldingPatternResponse(BaseSettings):
    promoters: Optional[Decimal]
    fii: Optional[Decimal]
    dii: Optional[Decimal]
    public: Optional[Decimal]
    others: Optional[Decimal]

class FinancialsOverviewResponse(BaseSettings):
    revenue: Optional[Decimal]
    expenses: Optional[Decimal]
    profit_loss: Optional[Decimal]
    assets: Optional[Decimal]
    liabilities: Optional[Decimal]
    equity: Optional[Decimal]

class DetailedFinancialsResponse(BaseSettings):
    balance_sheet: Dict[str, Decimal]
    profit_loss: Dict[str, Decimal]
    cash_flow: Dict[str, Decimal]

class StockManagementInfoResponse(BaseSettings):
    director: Optional[dict]
    chairman_and_managing_director: Optional[str]
    address: Optional[str]
    telephone: Optional[str]
    fax_number: Optional[str]
    email: Optional[str]
    website: Optional[str]

class StockWCategoryMappingResponse(BaseSettings):
    category: str
    exchange: str
    token: str
    name: str

    class Config:
        orm_mode = True

class StockExchangeHistPriceDataResponse(BaseSettings):
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

class StockIDWPCMappingResponse(BaseSettings):
    id: str
    identifier: str
    wpc: str
    wstockcode: str
    identifier_type: str

    class Config:
        orm_mode = True

class StockHistPriceDataResponse(BaseSettings):
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

class TechnicalIndicatorsResponse(BaseSettings):
    rsi: Optional[Decimal]
    macd: Optional[Decimal]
    ema: Optional[Decimal]
    sma: Optional[Decimal]
    std: Optional[Decimal]

class StockReturnsResponse(BaseSettings):
    one_month: Optional[Decimal]
    three_months: Optional[Decimal]
    six_months: Optional[Decimal]
    one_year: Optional[Decimal]
    two_years: Optional[Decimal]
    three_years: Optional[Decimal]
    five_years: Optional[Decimal]

class StockHistPriceDataBase(BaseSettings):
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

class StockNSEHistPriceDataSchema(BaseModel):
    wstockcode: str
    price_date: date
    open: Decimal = Decimal('0.000000')
    close: Decimal = Decimal('0.000000')
    low: Decimal = Decimal('0.000000')
    high: Decimal = Decimal('0.000000')
    volume: Decimal = Decimal('0.000000')
    value: Decimal = Decimal('0.000000')
    diff: Decimal = Decimal('0.000000')
    percentage_change: Decimal = Decimal('0.000000')

class StockBSEHistPriceDataSchema(BaseModel):
    wstockcode: str
    price_date: date
    open: Decimal = Decimal('0.000000')
    close: Decimal = Decimal('0.000000')
    low: Decimal = Decimal('0.000000')
    high: Decimal = Decimal('0.000000')
    volume: Decimal = Decimal('0.000000')
    value: Decimal = Decimal('0.000000')
    diff: Decimal = Decimal('0.000000')
    percentage_change: Decimal = Decimal('0.000000')

class StockManagementInfoSchema(BaseModel):
    wstockcode: str
    director: Optional[Dict]
    chairman_and_managing_director: Optional[str]
    address: Optional[str]
    telephone: Optional[str]
    fax_number: Optional[str]
    email: Optional[str]
    website: Optional[str]

class StockWCategoryMappingSchema(BaseModel):
    category: str
    exchange: str = 'nse'
    token: str
    name: str

class StockIDWPCMappingSchema(BaseModel):
    identifier: str
    wpc: str
    wstockcode: str
    identifier_type: str

class StockYearlyRatioHistDataSchema(BaseModel):
    wstockcode: str
    rtype: Optional[WResultType]
    as_on: Optional[date]
    pe: Decimal = Decimal('0.000')
    pb: Decimal = Decimal('0.000')
    dividend_yield: Decimal = Decimal('0.000')
    dividend_payout: Decimal = Decimal('0.000')
    eps: Decimal = Decimal('0.000')
    book_value: Decimal = Decimal('0.000')
    roa: Decimal = Decimal('0.000')
    roe: Decimal = Decimal('0.000')
    roce: Decimal = Decimal('0.000')
    asset_turnover: Decimal = Decimal('0.000')
    current_ratio: Decimal = Decimal('0.000')
    debt_to_equity: Decimal = Decimal('0.000')

class StockShareHoldingHistDataSchema(BaseModel):
    wstockcode: str
    year: Optional[int]
    month: Optional[int]
    total_holdings: Decimal = Decimal('0.000')
    promoter_ts: Decimal = Decimal('0.000')
    non_promoter_ts: Decimal = Decimal('0.000')
    non_promoter_inst_ts: Decimal = Decimal('0.000')
    non_promoter_non_inst_ts: Decimal = Decimal('0.000')
    custodians_ts: Decimal = Decimal('0.000')
    promoters_fcb_ts: Decimal = Decimal('0.000')
    promoters_fcb_tps: Decimal = Decimal('0.000')
    promoters_f_ind_nri_ts: Decimal = Decimal('0.000')
    promoters_f_ind_nri_tps: Decimal = Decimal('0.000')
    promoters_f_inst_ts: Decimal = Decimal('0.000')
    promoters_f_inst_tps: Decimal = Decimal('0.000')
    promoters_f_others_ts: Decimal = Decimal('0.000')
    promoters_f_others_tps: Decimal = Decimal('0.000')
    promoters_indian_ts: Decimal = Decimal('0.000')
    promoters_indian_tps: Decimal = Decimal('0.000')
    promoters_indian_govt_ts: Decimal = Decimal('0.000')
    promoters_indian_govt_tps: Decimal = Decimal('0.000')
    promoters_icb_ts: Decimal = Decimal('0.000')
    promoters_icb_tps: Decimal = Decimal('0.000')
    promoters_indian_directors_ts: Decimal = Decimal('0.000')
    promoters_indian_directors_tps: Decimal = Decimal('0.000')
    promoters_individual_huf_ts: Decimal = Decimal('0.000')
    promoters_individual_huf_tps: Decimal = Decimal('0.000')
    promoters_financial_inst_ts: Decimal = Decimal('0.000')
    promoters_financial_inst_tps: Decimal = Decimal('0.000')
    promoters_partnership_firm_ts: Decimal = Decimal('0.000')
    promoters_partnership_firm_tps: Decimal = Decimal('0.000')
    promoters_pac_ts: Decimal = Decimal('0.000')
    promoters_pac_tps: Decimal = Decimal('0.000')
    promoters_trust_ts: Decimal = Decimal('0.000')
    promoters_trust_tps: Decimal = Decimal('0.000')
    promoters_others_ts: Decimal = Decimal('0.000')
    promoters_others_tps: Decimal = Decimal('0.000')
    govt_ts: Decimal = Decimal('0.000')
    foreign_direct_inv_ts: Decimal = Decimal('0.000')
    foreign_inst_inv_ts: Decimal = Decimal('0.000')
    foreign_bank_ts: Decimal = Decimal('0.000')
    foreign_vci_ts: Decimal = Decimal('0.000')
    foreign_inst_others_ts: Decimal = Decimal('0.000')
    foreign_collaborators_ts: Decimal = Decimal('0.000')
    foreign_bodies_corporate_ts: Decimal = Decimal('0.000')
    mutual_fund_ts: Decimal = Decimal('0.000')
    financial_inst_bank_ts: Decimal = Decimal('0.000')
    insurance_co_ts: Decimal = Decimal('0.000')
    dii_others_ts: Decimal = Decimal('0.000')
    dii_trust_ts: Decimal = Decimal('0.000')
    venture_capital_ts: Decimal = Decimal('0.000')
    dii_corporate_bodies_ts: Decimal = Decimal('0.000')
    nsdl_intransit_ts: Decimal = Decimal('0.000')
    dii_clearing_members_ts: Decimal = Decimal('0.000')
    directors_and_relatives_ts: Decimal = Decimal('0.000')
    employees_ts: Decimal = Decimal('0.000')
    iut1l_ts: Decimal = Decimal('0.000')
    ia1l_ts: Decimal = Decimal('0.000')
    nri_ts: Decimal = Decimal('0.000')
    huf_ts: Decimal = Decimal('0.000')
    corporate_bodies_ts: Decimal = Decimal('0.000')
    societies_ts: Decimal = Decimal('0.000')
    trust_ts: Decimal = Decimal('0.000')
    others_ts: Decimal = Decimal('0.000')
    foreign_corporate_bodies_ts: Decimal = Decimal('0.000')
    foreign_non_inst_others_ts: Decimal = Decimal('0.000')
    shares_intransit_ts: Decimal = Decimal('0.000')
    nsdl_transit_ts: Decimal = Decimal('0.000')
    market_maker_ts: Decimal = Decimal('0.000')
    escrow_account_ts: Decimal = Decimal('0.000')
    clearing_members_ts: Decimal = Decimal('0.000')
    gdr_ts: Decimal = Decimal('0.000')
    adr_ts: Decimal = Decimal('0.000')
    other_custodians_ts: Decimal = Decimal('0.000')
    total_promoter_per_pledge_shares: Decimal = Decimal('0.000')

class StockBonusHistDataSchema(BaseModel):
    wstockcode: str
    announcement_date: date
    ex_bonus_date: date
    ratio: str


class StockRightsHistDataSchema(BaseModel):
    wstockcode: str
    ex_right_date: date
    ratio: str
    premium: Decimal = Decimal('0.00')

class StockBoardMeetingHistDataSchema(BaseModel):
    wstockcode: str
    meeting_date: date
    meeting_type: str  # AGM or EGM
    agenda: str

class StockFinancialQuarterlyResultSchema(BaseModel):
    wstockcode: str
    rtype: Optional[WResultType]
    as_on: date
    total_income: Decimal = Decimal('0.00')
    total_expenses: Decimal = Decimal('0.00')
    profit_before_tax: Decimal = Decimal('0.00')
    profit_after_tax: Decimal = Decimal('0.00')
    earnings_per_share: Decimal = Decimal('0.00')
    dividend_per_share: Decimal = Decimal('0.00')
    net_worth: Decimal = Decimal('0.00')
    total_assets: Decimal = Decimal('0.00')
    total_liabilities: Decimal = Decimal('0.00')

class StockFinancialHalfYearlyResultSchema(BaseModel):
    wstockcode: str
    rtype: Optional[WResultType]
    as_on: date
    total_income: Decimal = Decimal('0.00')
    total_expenses: Decimal = Decimal('0.00')
    profit_before_tax: Decimal = Decimal('0.00')
    profit_after_tax: Decimal = Decimal('0.00')
    earnings_per_share: Decimal = Decimal('0.00')
    dividend_per_share: Decimal = Decimal('0.00')
    net_worth: Decimal = Decimal('0.00')
    total_assets: Decimal = Decimal('0.00')
    total_liabilities: Decimal = Decimal('0.00')

class StockFinancialNineMonthResultSchema(BaseModel):
    wstockcode: str
    rtype: Optional[WResultType]
    as_on: date
    total_income: Decimal = Decimal('0.00')
    total_expenses: Decimal = Decimal('0.00')
    profit_before_tax: Decimal = Decimal('0.00')
    profit_after_tax: Decimal = Decimal('0.00')
    earnings_per_share: Decimal = Decimal('0.00')
    dividend_per_share: Decimal = Decimal('0.00')
    net_worth: Decimal = Decimal('0.00')
    total_assets: Decimal = Decimal('0.00')
    total_liabilities: Decimal = Decimal('0.00')

class StockBalanceSheetSchema(BaseModel):
    wstockcode: str
    as_on: date
    rtype: Optional[WResultType]
    share_capital: Decimal = Decimal('0.00')
    reserves_and_surplus: Decimal = Decimal('0.00')
    total_shareholders_funds: Decimal = Decimal('0.00')
    long_term_borrowings: Decimal = Decimal('0.00')
    deferred_tax_liabilities: Decimal = Decimal('0.00')
    other_long_term_liabilities: Decimal = Decimal('0.00')
    total_non_current_liabilities: Decimal = Decimal('0.00')
    short_term_borrowings: Decimal = Decimal('0.00')
    trade_payables: Decimal = Decimal('0.00')
    other_current_liabilities: Decimal = Decimal('0.00')
    short_term_provisions: Decimal = Decimal('0.00')
    total_current_liabilities: Decimal = Decimal('0.00')
    total_equity_and_liabilities: Decimal = Decimal('0.00')
    fixed_assets: Decimal = Decimal('0.00')
    non_current_investments: Decimal = Decimal('0.00')
    deferred_tax_assets: Decimal = Decimal('0.00')
    long_term_loans_and_advances: Decimal = Decimal('0.00')
    other_non_current_assets: Decimal = Decimal('0.00')
    total_non_current_assets: Decimal = Decimal('0.00')
    inventories: Decimal = Decimal('0.00')
    trade_receivables: Decimal = Decimal('0.00')
    cash_and_bank_balances: Decimal = Decimal('0.00')
    short_term_loans_and_advances: Decimal = Decimal('0.00')
    other_current_assets: Decimal = Decimal('0.00')
    total_current_assets: Decimal = Decimal('0.00')
    total_assets: Decimal = Decimal('0.00')

class StockBalanceSheetQuarterlySchema(BaseModel):
    wstockcode: str
    as_on: date
    rtype: Optional[WResultType]
    share_capital: Decimal = Decimal('0.00')
    reserves_and_surplus: Decimal = Decimal('0.00')
    total_shareholders_funds: Decimal = Decimal('0.00')
    long_term_borrowings: Decimal = Decimal('0.00')
    deferred_tax_liabilities: Decimal = Decimal('0.00')
    other_long_term_liabilities: Decimal = Decimal('0.00')
    total_non_current_liabilities: Decimal = Decimal('0.00')
    short_term_borrowings: Decimal = Decimal('0.00')
    trade_payables: Decimal = Decimal('0.00')
    other_current_liabilities: Decimal = Decimal('0.00')
    short_term_provisions: Decimal = Decimal('0.00')
    total_current_liabilities: Decimal = Decimal('0.00')
    total_equity_and_liabilities: Decimal = Decimal('0.00')
    fixed_assets: Decimal = Decimal('0.00')
    non_current_investments: Decimal = Decimal('0.00')
    deferred_tax_assets: Decimal = Decimal('0.00')
    long_term_loans_and_advances: Decimal = Decimal('0.00')
    other_non_current_assets: Decimal = Decimal('0.00')
    total_non_current_assets: Decimal = Decimal('0.00')
    inventories: Decimal = Decimal('0.00')
    trade_receivables: Decimal = Decimal('0.00')
    cash_and_bank_balances: Decimal = Decimal('0.00')
    short_term_loans_and_advances: Decimal = Decimal('0.00')
    other_current_assets: Decimal = Decimal('0.00')
    total_current_assets: Decimal = Decimal('0.00')
    total_assets: Decimal = Decimal('0.00')

class StockBalanceSheetHalfYearlySchema(BaseModel):
    wstockcode: str
    as_on: date
    rtype: Optional[WResultType]
    share_capital: Decimal = Decimal('0.00')
    reserves_and_surplus: Decimal = Decimal('0.00')
    total_shareholders_funds: Decimal = Decimal('0.00')
    long_term_borrowings: Decimal = Decimal('0.00')
    deferred_tax_liabilities: Decimal = Decimal('0.00')
    other_long_term_liabilities: Decimal = Decimal('0.00')
    total_non_current_liabilities: Decimal = Decimal('0.00')
    short_term_borrowings: Decimal = Decimal('0.00')
    trade_payables: Decimal = Decimal('0.00')
    other_current_liabilities: Decimal = Decimal('0.00')
    short_term_provisions: Decimal = Decimal('0.00')
    total_current_liabilities: Decimal = Decimal('0.00')
    total_equity_and_liabilities: Decimal = Decimal('0.00')
    fixed_assets: Decimal = Decimal('0.00')
    non_current_investments: Decimal = Decimal('0.00')
    deferred_tax_assets: Decimal = Decimal('0.00')
    long_term_loans_and_advances: Decimal = Decimal('0.00')
    other_non_current_assets: Decimal = Decimal('0.00')
    total_non_current_assets: Decimal = Decimal('0.00')
    inventories: Decimal = Decimal('0.00')
    trade_receivables: Decimal = Decimal('0.00')
    cash_and_bank_balances: Decimal = Decimal('0.00')
    short_term_loans_and_advances: Decimal = Decimal('0.00')
    other_current_assets: Decimal = Decimal('0.00')
    total_current_assets: Decimal = Decimal('0.00')
    total_assets: Decimal = Decimal('0.00')

class StockFinancialYearlyResultSchema(BaseModel):
    wstockcode: str
    rtype: Optional[WResultType]
    as_on: date
    total_income: Decimal = Decimal('0.00')
    total_expenses: Decimal = Decimal('0.00')
    profit_before_tax: Decimal = Decimal('0.00')
    profit_after_tax: Decimal = Decimal('0.00')
    earnings_per_share: Decimal = Decimal('0.00')
    dividend_per_share: Decimal = Decimal('0.00')
    net_worth: Decimal = Decimal('0.00')
    total_assets: Decimal = Decimal('0.00')
    total_liabilities: Decimal = Decimal('0.00')
    # Add any additional fields from the model if necessary.
