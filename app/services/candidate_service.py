"""Service Layer – CandidateService"""

from sqlalchemy.orm import Session
from app.repositories.candidate_repository import CandidateRepository
from app.models.candidate import Candidate
from app.schemas.candidate_schema import CandidateCreate


class CandidateService:

    def __init__(self):
        self.repo = CandidateRepository()

    def create_candidate(self, db: Session, data: CandidateCreate):
        candidate = Candidate(
            name=data.name,
            party_name=data.party_name,
            constituency_id=data.constituency_id,
        )
        return self.repo.create(db, candidate)

    def get_candidate(self, db: Session, candidate_id: int):
        candidate = self.repo.get_by_id(db, candidate_id)
        if not candidate:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail=f"Candidate {candidate_id} not found")
        return candidate

    def list_candidates(self, db: Session, constituency_id: int = None):
        if constituency_id:
            return self.repo.get_by_constituency(db, constituency_id)
        return self.repo.get_all(db)

    def delete_candidate(self, db: Session, candidate_id: int):
        candidate = self.get_candidate(db, candidate_id)
        self.repo.delete(db, candidate)
        return {"message": f"Candidate {candidate_id} deleted"}
