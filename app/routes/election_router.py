from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.election_schema import ElectionCreate, ElectionStatusUpdate
from app.services.election_service import ElectionService
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.admin import Admin

router = APIRouter()
service = ElectionService()


@router.post("/")
def create_election(
    election: ElectionCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    return service.create_election(db, election)


@router.get("/")
def list_elections(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return service.list_elections(db, status)


@router.get("/{election_id}")
def get_election(election_id: int, db: Session = Depends(get_db)):
    return service.get_election(db, election_id)


@router.patch("/{election_id}/status")
def update_election_status(
    election_id: int,
    body: ElectionStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    return service.update_status(db, election_id, body.status)


@router.delete("/{election_id}")
def delete_election(
    election_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    return service.delete_election(db, election_id)