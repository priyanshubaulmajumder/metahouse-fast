"""
from sqlalchemy import Column, Float, String, Boolean, Numeric, Date, DateTime, ForeignKey, Index, Integer, Text, Enum, JSON, UniqueConstraint, event
from sqlalchemy.orm import relationship, object_session
from sqlalchemy.sql import func
from app.db.base import Base
from app.utils.model_utils import WealthyProductCodeField, WealthyExternalIdField, generate_wealthy_stock_code
from decimal import Decimal
from enum import Enum as PyEnum

class StockCategory(PyEnum):
    LARGE_CAP = 'L'
    MID_CAP = 'M'
    SMALL_CAP = 'S'

class StockIDGenerator(Base):
    __tablename__ = "stock_id_generator"
    generated_id = Column(Integer, primary_key=True, autoincrement=True)

class Stock(Base):
    __tablename__ = "stocks"

    wstockcode = Column(String(28), primary_key=True)
    wpc = Column(WealthyProductCodeField("ST", StockIDGenerator, max_length=12), unique=True, nullable=True)
    third_party_id = Column(String(10))
    name = Column(String(256))
    bse_token = Column(String(50), nullable=True)
    bse_symbol = Column(String(50), nullable=True)
    nse_token = Column(String(50), nullable=True)
    nse_symbol = Column(String(50), nullable=True)
    nse_series = Column(String(50), nullable=True)
    instrument_type = Column(String(15), nullable=True)
    display_name = Column(String(256), nullable=True)
    isin = Column(String(20), nullable=True)
    sector = Column(String(100), nullable=True)
    industry = Column(String(100), nullable=True)
    category = Column(Enum(StockCategory), nullable=True)
    
    bse_lcp = Column(Numeric(20, 3), default=Decimal("0.000"))
    bse_lcp_date = Column(Date, nullable=True)
    nse_lcp = Column(Numeric(20, 3), default=Decimal("0.000"))
    nse_lcp_date = Column(Date, nullable=True)
    bse_latest_diff = Column(Numeric(20, 3), default=Decimal("0.000"))
    nse_latest_diff = Column(Numeric(20, 3), default=Decimal("0.000"))
    bse_latest_percentage_change = Column(Numeric(7, 3), default=Decimal("0.000"))
    nse_latest_percentage_change = Column(Numeric(7, 3), default=Decimal("0.000"))
    nse_hist_lcp_date = Column(Date, nullable=True)
    bse_hist_lcp_date = Column(Date, nullable=True)
    
    bse_52_week_high = Column(Numeric(20, 3), nullable=True)
    bse_52_week_low = Column(Numeric(20, 3), nullable=True)
    nse_52_week_high = Column(Numeric(20, 3), nullable=True)
    nse_52_week_low = Column(Numeric(20, 3), nullable=True)
    
    face_value = Column(Numeric(5, 3), default=Decimal("0.000"), nullable=True)
    market_cap = Column(Numeric(30, 3), default=Decimal("0.000"), nullable=True)
    no_of_shares = Column(Numeric(15, 1), default=Decimal("0.0"), nullable=True)
    
    beta = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    
    w_take_buy = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    w_take_hold = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    w_take_sell = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    wealthy_score = Column(Integer, nullable=True)
    hidden = Column(Boolean, default=False)
    is_listed = Column(Boolean, default=False)
    is_traded = Column(Boolean, default=False)
    deprecated_at = Column(DateTime, nullable=True)
    deprecate_reason = Column(String(254), nullable=True)
    
    #store historical prices
    historical_prices = relationship("StockHistPriceData", back_populates="stock")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

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

class StockHistPriceData(Base):
    __tablename__ = "stock_hist_price_data"

    id = Column(Integer, primary_key=True, index=True)
    wstockcode = Column(String, ForeignKey("stock.wstockcode"), index=True)
    date = Column(Date, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)   
    volume = Column(Integer)
    exchange = Column(String)

    stock = relationship("Stock", back_populates="historical_prices")

    class Config:
        orm_mode = True

class StockIDWPCMapping(Base):
    __tablename__ = "stock_id_wpc_mappings"

    id = Column(WealthyExternalIdField(prefix="siwm_"), primary_key=True)
    identifier = Column(String(50), nullable=False)
    wpc = Column(String(12), ForeignKey("stocks.wpc"))
    wstockcode = Column(String(28), ForeignKey("stocks.wstockcode"))
    identifier_type = Column(String(15), nullable=False)

    stock = relationship("Stock", foreign_keys=[wstockcode])

    __table_args__ = (
        Index('ix_siwm_identifier_909', 'identifier'),
        Index('ix_siwm_idtype_397', 'identifier_type'),
        UniqueConstraint('identifier', 'wpc', name='uq_siwm_identifier_wpc')
    )


@event.listens_for(Stock, 'before_insert')
def generate_wpc(mapper, connection, target):
    if target.wpc is None:
        session = object_session(target)
        target.wpc = WealthyProductCodeField.generate_code(session, "ST", StockIDGenerator, 12)

class StockManagementInfo(Base):
    __tablename__ = "stock_management_info"

    wstockcode = Column(String(28), ForeignKey('stocks.wstockcode'), primary_key=True)
    director = Column(JSON, nullable=True)
    chairman_and_managing_director = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    telephone = Column(String(18), nullable=True)
    fax_number = Column(String(12), nullable=True)
    email = Column(String(254), nullable=True)
    website = Column(String(50), nullable=True)

    stock = relationship("Stock", back_populates="management_info")

    __table_args__ = (
        Index('ix_smi_wstockcode_11', 'wstockcode'),
    )

class StockCachedNSEHPriceData(Base):
    __tablename__ = "stock_cached_nse_hprice_data"

    wstockcode = Column(String(28), ForeignKey('stocks.wstockcode'), primary_key=True)
    third_party_id = Column(String(10))
    name = Column(String(256))
    latest_price_date = Column(Date, nullable=True)
    prices = Column(JSON, nullable=True)

    stock = relationship("Stock", back_populates="nse_hprice_data")

    __table_args__ = (
        Index('ix_stock_nhp_thid_party_id_1', 'third_party_id'),
    )

class StockCachedBSEHPriceData(Base):
    __tablename__ = "stock_cached_bse_hprice_data"

    wstockcode = Column(String(28), ForeignKey('stocks.wstockcode'), primary_key=True)
    third_party_id = Column(String(10))
    name = Column(String(256))
    latest_price_date = Column(Date, nullable=True)
    prices = Column(JSON, nullable=True)

    stock = relationship("Stock", back_populates="bse_hprice_data")

    __table_args__ = (
        Index('ix_stock_bhp_thid_party_id_1', 'third_party_id'),
    )

class StockNSEHistPriceData(Base):
    __tablename__ = "stock_nse_hist_price_data"

    id = Column(Integer, primary_key=True)
    wstockcode = Column(String(28), ForeignKey('stocks.wstockcode'))
    price_date = Column(Date)
    open = Column(Numeric(20, 6), default=Decimal('0.000000'))
    close = Column(Numeric(20, 6), default=Decimal('0.000000'))
    low = Column(Numeric(20, 6), default=Decimal('0.000000'))
    high = Column(Numeric(20, 6), default=Decimal('0.000000'))
    volume = Column(Numeric(20, 6), default=Decimal('0.000000'))
    value = Column(Numeric(20, 6), default=Decimal('0.000000'))
    diff = Column(Numeric(20, 6), default=Decimal('0.000000'))
    percentage_change = Column(Numeric(20, 6), default=Decimal('0.000000'))

    stock = relationship("Stock", back_populates="nse_hist_price_data")

    __table_args__ = (
        Index('ix_snsehp_wstockcode_1', 'wstockcode'),
        Index('uq_snsehp_wstockcode_price_date', 'wstockcode', 'price_date', unique=True),
    )

class StockBSEHistPriceData(Base):
    __tablename__ = "stock_bse_hist_price_data"

    id = Column(Integer, primary_key=True)
    wstockcode = Column(String(28), ForeignKey('stocks.wstockcode'))
    price_date = Column(Date)
    open = Column(Numeric(20, 6), default=Decimal('0.000000'))
    close = Column(Numeric(20, 6), default=Decimal('0.000000'))
    low = Column(Numeric(20, 6), default=Decimal('0.000000'))
    high = Column(Numeric(20, 6), default=Decimal('0.000000'))
    volume = Column(Numeric(20, 6), default=Decimal('0.000000'))
    value = Column(Numeric(20, 6), default=Decimal('0.000000'))
    diff = Column(Numeric(20, 6), default=Decimal('0.000000'))
    percentage_change = Column(Numeric(20, 6), default=Decimal('0.000000'))

    stock = relationship("Stock", back_populates="bse_hist_price_data")

    __table_args__ = (
        Index('ix_sbsehp_wstockcode_1', 'wstockcode'),
        Index('uq_sbsehp_wstockcode_price_date', 'wstockcode', 'price_date', unique=True),
    )

class StockWCategoryMapping(Base):
    __tablename__ = "stock_wcategory_mapping"

    id = Column(Integer, primary_key=True)
    category = Column(String(10))
    exchange = Column(String(4), default="nse")
    token = Column(String(10))
    name = Column(String(256))

Stock.management_info = relationship("StockManagementInfo", back_populates="stock", uselist=False)
Stock.nse_hprice_data = relationship("StockCachedNSEHPriceData", back_populates="stock", uselist=False)
Stock.bse_hprice_data = relationship("StockCachedBSEHPriceData", back_populates="stock", uselist=False)
Stock.nse_hist_price_data = relationship("StockNSEHistPriceData", back_populates="stock")
Stock.bse_hist_price_data = relationship("StockBSEHistPriceData", back_populates="stock")
"""

from sqlalchemy import Column, Float, String, Boolean, Numeric, Date, DateTime, ForeignKey, Index, Integer, Text, Enum, JSON, UniqueConstraint, event
from sqlalchemy.orm import relationship, object_session
from sqlalchemy.sql import func
from app.db.base import Base
from app.utils.model_utils import WealthyProductCodeField, WealthyExternalIdField, generate_wealthy_stock_code
from decimal import Decimal
from enum import Enum as PyEnum

class StockCategory(PyEnum):
    LARGE_CAP = 'L'
    MID_CAP = 'M'
    SMALL_CAP = 'S'

class StockIDGenerator(Base):
    __tablename__ = "stock_id_generator"
    generated_id = Column(Integer, primary_key=True, autoincrement=True)

class Stock(Base):
    __tablename__ = "stocks"

    wstockcode = Column(String(28), primary_key=True)
    wpc = Column(WealthyProductCodeField("ST", StockIDGenerator, max_length=12), unique=True, nullable=True)
    third_party_id = Column(String(10))
    name = Column(String(256))
    bse_token = Column(String(50), nullable=True)
    bse_symbol = Column(String(50), nullable=True)
    nse_token = Column(String(50), nullable=True)
    nse_symbol = Column(String(50), nullable=True)
    nse_series = Column(String(50), nullable=True)
    instrument_type = Column(String(15), nullable=True)
    display_name = Column(String(256), nullable=True)
    isin = Column(String(20), nullable=True)
    sector = Column(String(100), nullable=True)
    industry = Column(String(100), nullable=True)
    category = Column(Enum(StockCategory), nullable=True)
    
    bse_lcp = Column(Numeric(20, 3), default=Decimal("0.000"))
    bse_lcp_date = Column(Date, nullable=True)
    nse_lcp = Column(Numeric(20, 3), default=Decimal("0.000"))
    nse_lcp_date = Column(Date, nullable=True)
    bse_latest_diff = Column(Numeric(20, 3), default=Decimal("0.000"))
    nse_latest_diff = Column(Numeric(20, 3), default=Decimal("0.000"))
    bse_latest_percentage_change = Column(Numeric(7, 3), default=Decimal("0.000"))
    nse_latest_percentage_change = Column(Numeric(7, 3), default=Decimal("0.000"))
    nse_hist_lcp_date = Column(Date, nullable=True)
    bse_hist_lcp_date = Column(Date, nullable=True)
    
    bse_52_week_high = Column(Numeric(20, 3), nullable=True)
    bse_52_week_low = Column(Numeric(20, 3), nullable=True)
    nse_52_week_high = Column(Numeric(20, 3), nullable=True)
    nse_52_week_low = Column(Numeric(20, 3), nullable=True)
    
    face_value = Column(Numeric(5, 3), default=Decimal("0.000"), nullable=True)
    market_cap = Column(Numeric(30, 3), default=Decimal("0.000"), nullable=True)
    no_of_shares = Column(Numeric(15, 1), default=Decimal("0.0"), nullable=True)
    
    beta = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    
    current_ratio = Column(Numeric(10, 3), default=Decimal("0.000"), nullable=True)
    debt_to_equity = Column(Numeric(10, 3), default=Decimal("0.000"), nullable=True)
    
    rsi = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    industry_pe_ratio = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    macd = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    ema = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    sma = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    std = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    
    returns_one_month = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    returns_three_months = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    returns_six_months = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    returns_one_year = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    returns_two_years = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    returns_three_years = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    returns_five_years = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    
    w_take_buy = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    w_take_hold = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    w_take_sell = Column(Numeric(20, 3), default=Decimal("0.000"), nullable=True)
    wealthy_score = Column(Integer, nullable=True)
    hidden = Column(Boolean, default=False)
    is_listed = Column(Boolean, default=False)
    is_traded = Column(Boolean, default=False)
    deprecated_at = Column(DateTime, nullable=True)
    deprecate_reason = Column(String(254), nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

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

class StockCachedNSEHPriceData(Base):
    __tablename__ = "stock_cached_nse_hprice_data"

    wstockcode = Column(String(28), ForeignKey('stocks.wstockcode'), primary_key=True)
    third_party_id = Column(String(10))
    name = Column(String(256))
    latest_price_date = Column(Date, nullable=True)
    prices = Column(JSON, nullable=True)

    stock = relationship("Stock", back_populates="nse_hprice_data")

    __table_args__ = (
        Index('ix_stock_nhp_thid_party_id_1', 'third_party_id'),
    )

class StockCachedBSEHPriceData(Base):
    __tablename__ = "stock_cached_bse_hprice_data"

    wstockcode = Column(String(28), ForeignKey('stocks.wstockcode'), primary_key=True)
    third_party_id = Column(String(10))
    name = Column(String(256))
    latest_price_date = Column(Date, nullable=True)
    prices = Column(JSON, nullable=True)

    stock = relationship("Stock", back_populates="bse_hprice_data")

    __table_args__ = (
        Index('ix_stock_bhp_thid_party_id_1', 'third_party_id'),
    )

class StockNSEHistPriceData(Base):
    __tablename__ = "stock_nse_hist_price_data"

    id = Column(Integer, primary_key=True)
    wstockcode = Column(String(28), ForeignKey('stocks.wstockcode'))
    price_date = Column(Date)
    open = Column(Numeric(20, 6), default=Decimal('0.000000'))
    close = Column(Numeric(20, 6), default=Decimal('0.000000'))
    low = Column(Numeric(20, 6), default=Decimal('0.000000'))
    high = Column(Numeric(20, 6), default=Decimal('0.000000'))
    volume = Column(Numeric(20, 6), default=Decimal('0.000000'))
    value = Column(Numeric(20, 6), default=Decimal('0.000000'))
    diff = Column(Numeric(20, 6), default=Decimal('0.000000'))
    percentage_change = Column(Numeric(20, 6), default=Decimal('0.000000'))

    stock = relationship("Stock", back_populates="nse_hist_price_data")

    __table_args__ = (
        Index('ix_snsehp_wstockcode_1', 'wstockcode'),
        UniqueConstraint('wstockcode', 'price_date', name='uq_snsehp_wstockcode_price_date'),
    )

class StockBSEHistPriceData(Base):
    __tablename__ = "stock_bse_hist_price_data"

    id = Column(Integer, primary_key=True)
    wstockcode = Column(String(28), ForeignKey('stocks.wstockcode'))
    price_date = Column(Date)
    open = Column(Numeric(20, 6), default=Decimal('0.000000'))
    close = Column(Numeric(20, 6), default=Decimal('0.000000'))
    low = Column(Numeric(20, 6), default=Decimal('0.000000'))
    high = Column(Numeric(20, 6), default=Decimal('0.000000'))
    volume = Column(Numeric(20, 6), default=Decimal('0.000000'))
    value = Column(Numeric(20, 6), default=Decimal('0.000000'))
    diff = Column(Numeric(20, 6), default=Decimal('0.000000'))
    percentage_change = Column(Numeric(20, 6), default=Decimal('0.000000'))

    stock = relationship("Stock", back_populates="bse_hist_price_data")

    __table_args__ = (
        Index('ix_sbsehp_wstockcode_1', 'wstockcode'),
        UniqueConstraint('wstockcode', 'price_date', name='uq_sbsehp_wstockcode_price_date'),
    )

class StockManagementInfo(Base):
    __tablename__ = "stock_management_info"

    wstockcode = Column(String(28), ForeignKey('stocks.wstockcode'), primary_key=True)
    director = Column(JSON, nullable=True)
    chairman_and_managing_director = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    telephone = Column(String(18), nullable=True)
    fax_number = Column(String(12), nullable=True)
    email = Column(String(254), nullable=True)
    website = Column(String(50), nullable=True)

    stock = relationship("Stock", back_populates="management_info")

    __table_args__ = (
        Index('ix_smi_wstockcode_11', 'wstockcode'),
    )
    
class StockWCategoryMapping(Base):
    __tablename__ = "stock_wcategory_mapping"

    id = Column(Integer, primary_key=True)
    category = Column(String(10))
    exchange = Column(String(4), default="nse")
    token = Column(String(10))
    name = Column(String(256))

Stock.management_info = relationship("StockManagementInfo", back_populates="stock", uselist=False)
Stock.nse_hprice_data = relationship("StockCachedNSEHPriceData", back_populates="stock", uselist=False)
Stock.bse_hprice_data = relationship("StockCachedBSEHPriceData", back_populates="stock", uselist=False)
Stock.nse_hist_price_data = relationship("StockNSEHistPriceData", back_populates="stock")
Stock.bse_hist_price_data = relationship("StockBSEHistPriceData", back_populates="stock")

@event.listens_for(Stock, 'before_insert')
def generate_wpc(mapper, connection, target):
    if target.wpc is None:
        session = object_session(target)
        target.wpc = WealthyProductCodeField.generate_code(session, "ST", StockIDGenerator, 12)
