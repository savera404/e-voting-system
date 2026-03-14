from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.candidate_schema import CandidateCreate
from app.services.candidate_service import CandidateService
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.admin import Admin

router = APIRouter()
service = CandidateService()


@router.post("/")
def create_candidate(
    candidate: CandidateCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    return service.create_candidate(db, candidate)


@router.get("/")
def list_candidates(
    constituency_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return service.list_candidates(db, constituency_id)


@router.get("/{candidate_id}")
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    return service.get_candidate(db, candidate_id)


@router.delete("/{candidate_id}")
def delete_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    return service.delete_candidate(db, candidate_id)