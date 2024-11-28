from datetime import date, datetime, timedelta
from decimal import Decimal

def create_test_stock():
    return {
        "wstockcode": "TEST_STOCK_001",
        "wpc": "ST00000001",
        "third_party_id": "TEST001",
        "name": "Test Stock Company",
        "bse_token": "500800",
        "bse_symbol": "TCS",
        "nse_token": "TCS",
        "nse_symbol": "TCS",
        "nse_series": "EQ",
        "instrument_type": "Stock",
        "display_name": "Test Company Services Ltd.",
        "isin": "INE467B01029",
        "sector": "Technology",
        "industry": "Software",
        "category": "L",
        "bse_lcp": Decimal("3500.00"),
        "bse_lcp_date": date.today(),
        "nse_lcp": Decimal("3502.00"),
        "nse_lcp_date": date.today(),
        "bse_latest_diff": Decimal("50.00"),
        "nse_latest_diff": Decimal("52.00"),
        "bse_latest_percentage_change": Decimal("1.45"),
        "nse_latest_percentage_change": Decimal("1.51"),
        "bse_52_week_high": Decimal("3900.00"),
        "bse_52_week_low": Decimal("3000.00"),
        "nse_52_week_high": Decimal("3905.00"),
        "nse_52_week_low": Decimal("2995.00"),
        "face_value": Decimal("1.000"),
        "market_cap": Decimal("1280000000000.000"),
        "no_of_shares": Decimal("3669760000.0"),
        "beta": Decimal("0.85"),
        "current_ratio": Decimal("3.45"),
        "debt_to_equity": Decimal("0.12"),
        "rsi": Decimal("65.5"),
        "industry_pe_ratio": Decimal("28.5"),
        "macd": Decimal("12.3"),
        "ema": Decimal("3480.5"),
        "sma": Decimal("3450.2"),
        "std": Decimal("120.5"),
        "returns_one_month": Decimal("2.5"),
        "returns_three_months": Decimal("5.8"),
        "returns_six_months": Decimal("12.3"),
        "returns_one_year": Decimal("18.5"),
        "returns_two_years": Decimal("45.2"),
        "returns_three_years": Decimal("75.8"),
        "returns_five_years": Decimal("125.5"),
        "w_take_buy": Decimal("3400.000"),
        "w_take_hold": Decimal("3500.000"),
        "w_take_sell": Decimal("3600.000"),
        "wealthy_score": 85,
        "hidden": False,
        "is_listed": True,
        "is_traded": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

def create_test_historical_prices(wstockcode: str, days: int = 30):
    prices = []
    base_date = date.today()
    base_price = Decimal("3500.00")
    
    for i in range(days):
        current_date = base_date - timedelta(days=i)
        price = {
            "wstockcode": wstockcode,
            "price_date": current_date,
            "open": base_price + Decimal(str(i)),
            "close": base_price + Decimal(str(i + 1)),
            "low": base_price + Decimal(str(i - 1)),
            "high": base_price + Decimal(str(i + 2)),
            "volume": Decimal("1000000"),
            "value": Decimal("3500000000"),
            "diff": Decimal("15.00"),
            "percentage_change": Decimal("0.43")
        }
        prices.append(price)
    return prices

def create_test_fundamentals():
    return {
        "pe": Decimal("25.8"),
        "pb": Decimal("5.2"),
        "dividend_yield": Decimal("1.8"),
        "dividend_payout": Decimal("45.5"),
        "eps": Decimal("135.2"),
        "book_value": Decimal("672.5"),
        "roa": Decimal("18.5"),
        "roe": Decimal("25.8"),
        "roce": Decimal("32.5"),
        "asset_turnover": Decimal("1.2"),
        "current_ratio": Decimal("3.45"),
        "debt_to_equity": Decimal("0.12"),
        "industry_pe_ratio": Decimal("28.5")
    }

def create_test_shareholding_pattern():
    return {
        "promoters": Decimal("72.5"),
        "fii": Decimal("12.8"),
        "dii": Decimal("8.5"),
        "public": Decimal("4.2"),
        "others": Decimal("2.0")
    } 