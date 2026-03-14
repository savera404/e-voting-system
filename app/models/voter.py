from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Voter(Base):
    __tablename__ = "voters"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    father_or_husband_name = Column(String, nullable=False)

    cnic = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True)

    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    constituency_id = Column(Integer, ForeignKey("constituencies.id"))

    has_voted = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    constituency = relationship("Constituency")