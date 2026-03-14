"""Repository Pattern – ElectionRepository"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.election import Election


class ElectionRepository:

    def create(self, db: Session, election: Election) -> Election:
        db.add(election)
        db.commit()
        db.refresh(election)
        return election

    def get_by_id(self, db: Session, election_id: int) -> Optional[Election]:
        return db.query(Election).filter(Election.id == election_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Election]:
        return db.query(Election).offset(skip).limit(limit).all()

    def get_by_status(self, db: Session, status: str) -> List[Election]:
        return db.query(Election).filter(Election.status == status).all()

    def update_status(self, db: Session, election: Election, new_status: str) -> Election:
        election.status = new_status
        db.commit()
        db.refresh(election)
        return election

    def delete(self, db: Session, election: Election) -> None:
        db.delete(election)
        db.commit()
