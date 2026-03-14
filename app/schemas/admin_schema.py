from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


class AdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class AdminResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    created_at: Optional[datetime]


class AdminTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin_id: int
    name: str