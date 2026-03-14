from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base


class Election(Base):
    __tablename__ = "elections"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    type = Column(String)           # "federal" | "provincial"
    status = Column(String, default="upcoming")  # "upcoming" | "active" | "completed"

    start_date = Column(DateTime)
    end_date = Column(DateTime)
