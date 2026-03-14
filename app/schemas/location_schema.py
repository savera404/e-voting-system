from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProvinceCreate(BaseModel):
    name: str

class ProvinceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: Optional[str]


class CityCreate(BaseModel):
    name: str
    province_id: int

class CityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: Optional[str]
    province_id: Optional[int]


class DistrictCreate(BaseModel):
    name: str
    city_id: int

class DistrictResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    city_id: Optional[int]


class ConstituencyCreate(BaseModel):
    name: str
    type: str   # "federal" | "provincial"
    district_id: int

class ConstituencyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    type: Optional[str]
    district_id: Optional[int]
