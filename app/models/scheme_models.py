from sqlalchemy import Column, String, Boolean, Numeric, Date, DateTime, ForeignKey, Index, Integer, Text, Enum, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from app.utils.model_utils import WealthyProductCodeField, WealthyExternalIdField
from enum import Enum as PyEnum
from decimal import Decimal

class SchemeType(PyEnum):
    OPEN_ENDED = 'OE'
    CLOSE_ENDED = 'CE'
    INTERVAL = 'IN'

class LockInUnitType(PyEnum):
    Days = 'D'
    Months = 'M'
    Years = 'Y'

class SchemeIDGenerator(Base):
    __tablename__ = "scheme_id_generator"
    generated_id = Column(Integer, primary_key=True, autoincrement=True)

class Scheme(Base):
    __tablename__ = "schemes"

    wschemecode = Column(String(28), primary_key=True)
    wpc = Column(WealthyProductCodeField(prefix="MF", Modal=SchemeIDGenerator, max_length=12), unique=True)
    third_party_id = Column(String(10))
    isin = Column(String(20))
    isin_reinvestment = Column(String(20))
    third_party_amc = Column(String(10))
    class_code = Column(String(10))
    amfi_code = Column(String(20))
    scheme_code = Column(String(20))
    scheme_code_ptm = Column(String(20))
    scheme_code_dtm = Column(String(20))
    tpsl_scheme_code = Column(String(20))
    fund_family_code = Column(String(50))
    scheme_name = Column(String(255))
    benchmark = Column(String(255))
    benchmark_tpid = Column(String(10))
    display_name = Column(String(255))
    category = Column(String(255))
    scheme_type = Column(Enum(SchemeType))
    # Add other fields as needed

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index('ix_scheme_third_party_id', 'third_party_id'),
        Index('ix_scheme_isin', 'isin'),
        Index('ix_scheme_amfi_code', 'amfi_code'),
        Index('ix_scheme_scheme_code', 'scheme_code'),
        Index('ix_scheme_wpc', 'wpc'),
    )

class SchemeAudit(Base):
    __tablename__ = "scheme_audits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wpc = Column(String(12))
    wschemecode = Column(String(28))
    isin = Column(String(20))
    third_party_amc = Column(String(10))
    amfi_code = Column(String(20))
    scheme_code = Column(String(20))
    tpsl_scheme_code = Column(String(20))
    fund_family_code = Column(String(50))
    scheme_name = Column(String(255))
    benchmark = Column(String(255))
    category = Column(String(255))
    scheme_type = Column(Enum(SchemeType))
    aum = Column(Numeric(20, 4))
    lock_in_time = Column(Integer)
    lock_in_unit = Column(Enum(LockInUnitType))
    risk_o_meter_value = Column(String(50))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SchemeHolding(Base):
    __tablename__ = "scheme_holdings"

    external_id = Column(WealthyExternalIdField(prefix="sch_holding_"), primary_key=True)
    wpc = Column(String(12), ForeignKey("schemes.wpc"))
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

    scheme = relationship("Scheme", back_populates="holdings")

    __table_args__ = (
        Index('idx_sh_wpc_876', 'wpc'),
        Index('idx_sh_htpid_564', 'holding_third_party_id'),
        Index('idx_sh_sector_267', 'sector_name'),
        Index('idx_sh_rating_391', 'rating'),
        UniqueConstraint('wpc', 'holding_third_party_id', 'isin', name='uq_scheme_holding'),
    )

class WSchemeCodeWPCMapping(Base):
    __tablename__ = "wscheme_code_wpc_mapping"
    __table_args__ = (
        Index('ix_wwm_wsc', 'wschemecode'),
        Index('ix_wwm_wpc', 'wpc'),
        {'extend_existing': True}
    )

    external_id = Column(WealthyExternalIdField(prefix="wsc_wpc_map_"), primary_key=True)
    wschemecode = Column(String(28), nullable=False)
    wpc = Column(String(12), nullable=False)
    hidden = Column(Boolean, default=False)



class SchemeCodeWPCMapping(Base):
    __tablename__ = "scheme_code_wpc_mapping"

    external_id = Column(WealthyExternalIdField(prefix="sc_wpc_map_"), primary_key=True)
    scheme_code = Column(String(20), nullable=False)
    wpc = Column(String(12), nullable=False)
    hidden = Column(Boolean, default=False)

    __table_args__ = (
        Index('ix_swm_sc', 'scheme_code'),
        Index('ix_swm_wpc', 'wpc'),
    )

class WPCWPCMapping(Base):
    __tablename__ = "wpc_wpc_mapping"

    external_id = Column(WealthyExternalIdField(prefix="wpc_wpc_map_"), primary_key=True)
    wpc = Column(String(12), nullable=False)
    target_wpc = Column(String(12), nullable=False)
    hidden = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint('wpc', 'target_wpc', name='uq_wpc_target_wpc'),
        Index('ix_wwm_wpc_674', 'wpc'),
        Index('ix_wwm_twpc_292', 'target_wpc'),
    )

class ParentChildSchemeMapping(Base):
    __tablename__ = "parent_child_scheme_mapping"

    external_id = Column(WealthyExternalIdField(prefix="par_ch_sch_map_"), primary_key=True)
    child_wpc = Column(String(12), nullable=False)
    parent_wpc = Column(String(12), nullable=False)

    __table_args__ = (
        UniqueConstraint('child_wpc', 'parent_wpc', name='uq_child_parent_wpc'),
        Index('ix_prs_cwpc_981', 'child_wpc'),
        Index('ix_prc_pwpc_728', 'parent_wpc'),
    )

class SectorToWSectorMapping(Base):
    __tablename__ = "sector_to_wsector_mapping"

    external_id = Column(WealthyExternalIdField(prefix="sctwsc_map_"), primary_key=True)
    sector = Column(String(60), unique=True)
    wsector = Column(String(35))

    __table_args__ = (
        Index('ix_stwm_sct_587', 'sector'),
        Index('ix_stwm_wsct_785', 'wsector'),
    )

Scheme.holdings = relationship("SchemeHolding", back_populates="scheme")
