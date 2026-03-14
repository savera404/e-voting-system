"""Repository Pattern – LocationRepository (Province, City, District, Constituency)"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.location import Province, City, District, Constituency


class LocationRepository:

    # ── Province ──────────────────────────────────────────────────────────
    def create_province(self, db: Session, name: str) -> Province:
        obj = Province(name=name)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get_province(self, db: Session, province_id: int) -> Optional[Province]:
        return db.query(Province).filter(Province.id == province_id).first()

    def list_provinces(self, db: Session) -> List[Province]:
        return db.query(Province).all()

    # ── City ──────────────────────────────────────────────────────────────
    def create_city(self, db: Session, name: str, province_id: int) -> City:
        obj = City(name=name, province_id=province_id)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get_city(self, db: Session, city_id: int) -> Optional[City]:
        return db.query(City).filter(City.id == city_id).first()

    def list_cities(self, db: Session, province_id: Optional[int] = None) -> List[City]:
        q = db.query(City)
        if province_id:
            q = q.filter(City.province_id == province_id)
        return q.all()

    # ── District ──────────────────────────────────────────────────────────
    def create_district(self, db: Session, name: str, city_id: int) -> District:
        obj = District(name=name, city_id=city_id)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get_district(self, db: Session, district_id: int) -> Optional[District]:
        return db.query(District).filter(District.id == district_id).first()

    def list_districts(self, db: Session, city_id: Optional[int] = None) -> List[District]:
        q = db.query(District)
        if city_id:
            q = q.filter(District.city_id == city_id)
        return q.all()

    # ── Constituency ──────────────────────────────────────────────────────
    def create_constituency(
        self, db: Session, name: str, cons_type: str, district_id: int
    ) -> Constituency:
        obj = Constituency(name=name, type=cons_type, district_id=district_id)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get_constituency(self, db: Session, constituency_id: int) -> Optional[Constituency]:
        return db.query(Constituency).filter(Constituency.id == constituency_id).first()

    def list_constituencies(
        self, db: Session, district_id: Optional[int] = None
    ) -> List[Constituency]:
        q = db.query(Constituency)
        if district_id:
            q = q.filter(Constituency.district_id == district_id)
        return q.all()
