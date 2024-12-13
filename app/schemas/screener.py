from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ScreenerSource(str, Enum):
    Wealthy = 'wealthy'
    CMOTS = 'cmots'
    MorningStar = 'morning_star'

class ScreenerBase(BaseModel):
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

    model_config = ConfigDict(from_attributes=True)

class ScreenerCreate(ScreenerBase):
    pass

class ScreenerUpdate(ScreenerBase):
    pass

class ScreenerInDB(ScreenerBase):
    wpc: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ScreenerResponse(ScreenerInDB):
    pass

class ScreenerInstrumentBase(BaseModel):
    instruments: List[str] = Field(...)
    cols: List[str] = Field(default_factory=list)
    screener: str  # Changed from 'screener_wpc' to 'screener'

    model_config = ConfigDict(from_attributes=True)

class ScreenerInstrumentCreate(ScreenerInstrumentBase):
    pass

class ScreenerInstrumentUpdate(ScreenerInstrumentBase):
    pass

class ScreenerInstrumentInDB(ScreenerInstrumentBase):
    id: int
    screener: str  # Changed from 'screener_wpc' to 'screener'
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ScreenerInstrumentResponse(ScreenerInstrumentInDB):
    pass

class WSchemeCodeWPCMappingBase(BaseModel):
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

class ISINWPCMappingBase(BaseModel):
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

class SchemeCodeWPCMappingBase(BaseModel):
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

class ScreenerListResponse(BaseModel):
    id: str
    name: str
    screeners: List[ScreenerResponse]

class ScreenerWithInstrumentsResponse(BaseModel):
    screener: ScreenerResponse  # Ensure this field exists
    instruments: List[ScreenerInstrumentResponse]
    
    model_config = ConfigDict(from_attributes=True)
