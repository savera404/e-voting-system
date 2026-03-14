from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Province(Base):
    __tablename__ = "provinces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    cities = relationship("City", back_populates="province")


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    province_id = Column(Integer, ForeignKey("provinces.id"))

    province = relationship("Province", back_populates="cities")
    districts = relationship("District", back_populates="city")


class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship("City", back_populates="districts")
    constituencies = relationship("Constituency", back_populates="district")


class Constituency(Base):
    __tablename__ = "constituencies"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)  
    # Example: NA-241, PS-115

    type = Column(String)
    # federal or provincial

    district_id = Column(Integer, ForeignKey("districts.id"))

    district = relationship("District", back_populates="constituencies")