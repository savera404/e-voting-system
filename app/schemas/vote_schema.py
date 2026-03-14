from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CastVoteRequest(BaseModel):
    candidate_id: int
    election_id: int


class VoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    voter_id: Optional[int]
    candidate_id: Optional[int]
    election_id: Optional[int]
    timestamp: Optional[datetime]


class ElectionResultResponse(BaseModel):
    method: str
    total_votes: int
    winner: Optional[dict]
    ranked_candidates: list
    requires_runoff: Optional[bool] = None
    runoff_candidates: Optional[list] = None
