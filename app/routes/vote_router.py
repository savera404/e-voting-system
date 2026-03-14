from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.vote_schema import CastVoteRequest
from app.services.vote_service import VoteService
from app.core.database import get_db
from app.core.dependencies import get_current_voter
from app.models.voter import Voter

router = APIRouter()
service = VoteService()


@router.post("/cast")
def cast_vote(
    payload: CastVoteRequest,
    db: Session = Depends(get_db),
    current_voter: Voter = Depends(get_current_voter),
):
    return service.cast_vote(db, current_voter, payload)


@router.get("/results/{election_id}")
def get_results(
    election_id: int,
    counting_method: str = "fptp",
    db: Session = Depends(get_db),
):
    return service.get_results(db, election_id, counting_method)