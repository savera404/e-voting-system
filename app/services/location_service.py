"""Service Layer – LocationService"""

from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.location_repository import LocationRepository
from app.schemas.location_schema import (
    ProvinceCreate, CityCreate, DistrictCreate, ConstituencyCreate
)


class LocationService:

    def __init__(self):
        self.repo = LocationRepository()

    # Provinces
    def create_province(self, db: Session, data: ProvinceCreate):
        return self.repo.create_province(db, data.name)

    def list_provinces(self, db: Session):
        return self.repo.list_provinces(db)

    def get_province(self, db: Session, province_id: int):
        p = self.repo.get_province(db, province_id)
        if not p:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Province not found")
        return p

    # Cities
    def create_city(self, db: Session, data: CityCreate):
        return self.repo.create_city(db, data.name, data.province_id)

    def list_cities(self, db: Session, province_id: Optional[int] = None):
        return self.repo.list_cities(db, province_id)

    # Districts
    def create_district(self, db: Session, data: DistrictCreate):
        return self.repo.create_district(db, data.name, data.city_id)

    def list_districts(self, db: Session, city_id: Optional[int] = None):
        return self.repo.list_districts(db, city_id)

    # Constituencies
    def create_constituency(self, db: Session, data: ConstituencyCreate):
        return self.repo.create_constituency(db, data.name, data.type, data.district_id)

    def list_constituencies(self, db: Session, district_id: Optional[int] = None):
        return self.repo.list_constituencies(db, district_id)

    def get_constituency(self, db: Session, constituency_id: int):
        c = self.repo.get_constituency(db, constituency_id)
        if not c:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Constituency not found")
        return c
