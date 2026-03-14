from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.location_schema import (
    ProvinceCreate, CityCreate, DistrictCreate, ConstituencyCreate
)
from app.services.location_service import LocationService
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.admin import Admin

router = APIRouter()
service = LocationService()


# ── Provinces ──────────────────────────────────────────────────────────────

@router.post("/provinces")
def create_province(
    data: ProvinceCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    return service.create_province(db, data)


@router.get("/provinces")
def list_provinces(db: Session = Depends(get_db)):
    return service.list_provinces(db)


@router.get("/provinces/{province_id}")
def get_province(province_id: int, db: Session = Depends(get_db)):
    return service.get_province(db, province_id)


# ── Cities ─────────────────────────────────────────────────────────────────

@router.post("/cities")
def create_city(
    data: CityCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    return service.create_city(db, data)


@router.get("/cities")
def list_cities(province_id: Optional[int] = None, db: Session = Depends(get_db)):
    return service.list_cities(db, province_id)


# ── Districts ──────────────────────────────────────────────────────────────

@router.post("/districts")
def create_district(
    data: DistrictCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    return service.create_district(db, data)


@router.get("/districts")
def list_districts(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    return service.list_districts(db, city_id)


# ── Constituencies ─────────────────────────────────────────────────────────

@router.post("/constituencies")
def create_constituency(
    data: ConstituencyCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    return service.create_constituency(db, data)


@router.get("/constituencies")
def list_constituencies(district_id: Optional[int] = None, db: Session = Depends(get_db)):
    return service.list_constituencies(db, district_id)


@router.get("/constituencies/{constituency_id}")
def get_constituency(constituency_id: int, db: Session = Depends(get_db)):
    return service.get_constituency(db, constituency_id)