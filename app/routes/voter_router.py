from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.voter_schema import VoterCreate
from app.services.voter_service import VoterService
from app.core.database import get_db

router = APIRouter()

service = VoterService()

@router.post("/register")
def register_voter(voter: VoterCreate, db: Session = Depends(get_db)):
    return service.register_voter(db, voter)