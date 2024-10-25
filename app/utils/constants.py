from enum import Enum

class ExchangeChoices(str, Enum):
    NSE = "nse"
    BSE = "bse"

class WHistoricalStockPricesField(str, Enum):
    CmotsID = "cmots_id"
    CompanyName = "company_name"
    High = "high"
    Low = "low"
    Open = "open"
    Close = "close"
    Date = "date"
    Volume = "volume"
    Value = "value"


class FalconExchange(int, Enum):
    NSE = 1
    BSE = 3

class WResultType(str, Enum):
    Standalone = 'S'
    Consolidated = 'C'

class WResultPeriod(str, Enum):
    Quarterly = 'Q'
    HalfYearly = 'HY'
    NineMonth = 'NM'
    Yearly = 'Y'

class WFData(str, Enum):
    Revenue = 'revenue'
    Profit = 'profit'
    EBITDA = 'ebitda'

fdata_col_mapping = {
    WFData.Revenue: "total_income",
    WFData.Profit: "net_profit",
    WFData.EBITDA: "ebitda",
}

class StockIdType(str, Enum):
    ISIN = 'isin'
    WPC = 'wpc'
    ThirdPartyId = 'tp-id'
    ExchangeToken = 'exchange-token'
    ExchangeSymbol = 'exchange-symbol'

class WShareHoldingEntity(str, Enum):
    Overview = 'overview'
    Promoters = 'promoters'
    FII = 'fii'
    DII = 'dii'
    Others = 'others'

class WScreenerCategory(str, Enum):
    Main = 'main'

class ScreenerSource(str, Enum):
    Wealthy = 'wealthy'
    CMOTS = 'cmots'
    MorningStar = 'morning_star'

class WCompanyMasterField(str, Enum):
    CmotsID = "cmots_id"
    BSECode = "bse_code"
    NSESymbol = "nse_symbol"
    CompanyName = "company_name"
    CompanyShortName = "company_short_name"
    CategoryName = "category_name"
    ISIN = "isin"
    BSEGroup = "bse_group"
    MCapType = "mcap_type"
    SectorCode = "sector_code"
    SectorName = "sector_name"
    IndustryCode = "industry_code"
    IndustryName = "industry_name"
    BSEListedFlag = "bse_listed_flag"
    NSEListedFlag = "nse_listed_flag"
    DisplayType = "display_type"