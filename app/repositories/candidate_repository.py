"""Repository Pattern – CandidateRepository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.candidate import Candidate


class CandidateRepository:

    def create(self, db: Session, candidate: Candidate) -> Candidate:
        db.add(candidate)
        db.commit()
        db.refresh(candidate)
        return candidate

    def get_by_id(self, db: Session, candidate_id: int) -> Optional[Candidate]:
        return db.query(Candidate).filter(Candidate.id == candidate_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Candidate]:
        return db.query(Candidate).offset(skip).limit(limit).all()

    def get_by_constituency(self, db: Session, constituency_id: int) -> List[Candidate]:
        return (
            db.query(Candidate)
            .filter(Candidate.constituency_id == constituency_id)
            .all()
        )

    def delete(self, db: Session, candidate: Candidate) -> None:
        db.delete(candidate)
        db.commit()
