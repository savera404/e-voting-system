from typing import Optional
from pydantic import BaseModel, ConfigDict


class CandidateCreate(BaseModel):
    name: str
    party_name: Optional[str] = None
    constituency_id: int


class CandidateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    party_name: Optional[str]
    constituency_id: Optional[int]
