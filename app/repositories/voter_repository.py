"""
Repository Pattern – VoterRepository (extended)
Centralises all voter-related DB queries.
"""

from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.voter import Voter


class VoterRepository:

    def create_voter(self, db: Session, voter_data) -> Voter:
        voter = Voter(**voter_data.dict())
        db.add(voter)
        db.commit()
        db.refresh(voter)
        return voter

    def get_by_id(self, db: Session, voter_id: int) -> Optional[Voter]:
        return db.query(Voter).filter(Voter.id == voter_id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[Voter]:
        return db.query(Voter).filter(Voter.email == email).first()

    def get_by_cnic(self, db: Session, cnic: str) -> Optional[Voter]:
        return db.query(Voter).filter(Voter.cnic == cnic).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Voter]:
        return db.query(Voter).offset(skip).limit(limit).all()

    def mark_voted(self, db: Session, voter: Voter) -> Voter:
        voter.has_voted = True
        db.commit()
        db.refresh(voter)
        return voter

    # Alias kept for backwards-compatibility with existing voter_service.py
    def get_voter_by_email(self, db: Session, email: str) -> Optional[Voter]:
        return self.get_by_email(db, email)
