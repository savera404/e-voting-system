from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class VoterCreate(BaseModel):
    name: str
    father_or_husband_name: str
    cnic: str
    phone_number: Optional[str] = None
    constituency_id: int
    email: EmailStr
    password: str


class VoterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    cnic: str
    email: str
    constituency_id: Optional[int]
    has_voted: bool
    created_at: Optional[datetime]


class VoterLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    voter_id: int
    name: str
