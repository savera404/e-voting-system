"""Repository Pattern – VoteRepository"""

from typing import List, Optional, Dict, Any
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.vote import Vote
from app.models.candidate import Candidate


class VoteRepository:

    def create(self, db: Session, vote: Vote) -> Vote:
        db.add(vote)
        db.commit()
        db.refresh(vote)
        return vote

    def get_by_id(self, db: Session, vote_id: int) -> Optional[Vote]:
        return db.query(Vote).filter(Vote.id == vote_id).first()

    def get_by_voter_and_election(
        self, db: Session, voter_id: int, election_id: int
    ) -> Optional[Vote]:
        return (
            db.query(Vote)
            .filter(Vote.voter_id == voter_id, Vote.election_id == election_id)
            .first()
        )

    def get_by_election(self, db: Session, election_id: int) -> List[Vote]:
        return db.query(Vote).filter(Vote.election_id == election_id).all()

    def get_vote_counts_for_election(
        self, db: Session, election_id: int
    ) -> List[Dict[str, Any]]:
        """
        Returns a list of dicts:
        [{"candidate_id": .., "name": .., "party": .., "votes": ..}, ...]
        """
        rows = (
            db.query(
                Candidate.id.label("candidate_id"),
                Candidate.name.label("name"),
                Candidate.party_name.label("party"),
                func.count(Vote.id).label("votes"),
            )
            .join(Vote, Vote.candidate_id == Candidate.id, isouter=True)
            .filter(Vote.election_id == election_id)
            .group_by(Candidate.id, Candidate.name, Candidate.party_name)
            .all()
        )
        return [
            {
                "candidate_id": r.candidate_id,
                "name": r.name,
                "party": r.party or "Independent",
                "votes": r.votes,
            }
            for r in rows
        ]

    def count_for_election(self, db: Session, election_id: int) -> int:
        return (
            db.query(func.count(Vote.id))
            .filter(Vote.election_id == election_id)
            .scalar()
            or 0
        )
