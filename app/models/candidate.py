from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    party_name = Column(String)

    constituency_id = Column(Integer, ForeignKey("constituencies.id"))

    constituency = relationship("Constituency")