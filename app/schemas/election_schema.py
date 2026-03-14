from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ElectionCreate(BaseModel):
    name: str
    type: str           # "federal" | "provincial" | "local"
    start_date: datetime
    end_date: datetime
    status: str = "upcoming"


class ElectionStatusUpdate(BaseModel):
    status: str         # "upcoming" | "active" | "completed"


class ElectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: Optional[str]
    status: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
