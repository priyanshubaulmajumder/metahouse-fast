from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ScreenerSource(str, Enum):
    Wealthy = 'wealthy'
    CMOTS = 'cmots'
    MorningStar = 'morning_star'

class ScreenerBase(BaseSettings):
    name: str = Field(..., max_length=254)
    source: ScreenerSource = Field(default=ScreenerSource.Wealthy)
    category: str = Field(..., max_length=254)
    category_display_name: str = Field(..., max_length=254)
    instrument_type: str = Field(..., max_length=254)
    description: Optional[str] = None
    refresh_rate: int = Field(default=24 * 60 * 60)
    additional_data: List[Any] = Field(default_factory=list)
    query_params: Dict[str, Any] = Field(default_factory=dict)
    uri: str
    is_active: bool = Field(default=False)
    order: int = Field(default=1)
    category_order: int = Field(default=1)

class ScreenerCreate(ScreenerBase):
    pass

class ScreenerUpdate(ScreenerBase):
    pass

class ScreenerInDB(ScreenerBase):
    wpc: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ScreenerResponse(ScreenerInDB):
    pass

class ScreenerInstrumentBase(BaseSettings):
    instruments: List[str] = Field(...)
    cols: List[str] = Field(default_factory=list)

class ScreenerInstrumentCreate(ScreenerInstrumentBase):
    screener_wpc: str

class ScreenerInstrumentUpdate(ScreenerInstrumentBase):
    pass

class ScreenerInstrumentInDB(ScreenerInstrumentBase):
    id: int
    screener_wpc: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ScreenerInstrumentResponse(ScreenerInstrumentInDB):
    pass

class WSchemeCodeWPCMappingBase(BaseSettings):
    wschemecode: str = Field(..., max_length=28)
    wpc: str = Field(..., max_length=12)
    hidden: bool = Field(default=False)

class WSchemeCodeWPCMappingCreate(WSchemeCodeWPCMappingBase):
    pass

class WSchemeCodeWPCMappingUpdate(WSchemeCodeWPCMappingBase):
    pass

class WSchemeCodeWPCMappingInDB(WSchemeCodeWPCMappingBase):
    external_id: str

    class Config:
        orm_mode = True

class WSchemeCodeWPCMappingResponse(WSchemeCodeWPCMappingInDB):
    pass

class ISINWPCMappingBase(BaseSettings):
    isin: str = Field(..., max_length=20)
    wpc: str = Field(..., max_length=12)
    hidden: bool = Field(default=False)

class ISINWPCMappingCreate(ISINWPCMappingBase):
    pass

class ISINWPCMappingUpdate(ISINWPCMappingBase):
    pass

class ISINWPCMappingInDB(ISINWPCMappingBase):
    external_id: str

    class Config:
        orm_mode = True

class ISINWPCMappingResponse(ISINWPCMappingInDB):
    pass

class SchemeCodeWPCMappingBase(BaseSettings):
    scheme_code: str = Field(..., max_length=20)
    wpc: str = Field(..., max_length=12)
    hidden: bool = Field(default=False)

class SchemeCodeWPCMappingCreate(SchemeCodeWPCMappingBase):
    pass

class SchemeCodeWPCMappingUpdate(SchemeCodeWPCMappingBase):
    pass

class SchemeCodeWPCMappingInDB(SchemeCodeWPCMappingBase):
    external_id: str

    class Config:
        orm_mode = True

class SchemeCodeWPCMappingResponse(SchemeCodeWPCMappingInDB):
    pass

class ScreenerListResponse(BaseSettings):
    id: str
    name: str
    screeners: List[ScreenerResponse]
