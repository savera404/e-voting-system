"""
Service Layer – ElectionService
Uses: Factory Pattern (create), Observer Pattern (status changes)
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.repositories.election_repository import ElectionRepository
from app.patterns.factory.election_factory import ElectionFactory
from app.patterns.observer.election_observer import ElectionEventManager
from app.core.exceptions import ElectionNotFoundException
from app.schemas.election_schema import ElectionCreate


class ElectionService:

    def __init__(self):
        self.repo = ElectionRepository()
        self._event_manager = ElectionEventManager.get_instance()

    def create_election(self, db: Session, data: ElectionCreate):
        """Uses Factory Pattern to create the Election ORM object."""
        election_obj = ElectionFactory.create(
            name=data.name,
            election_type=data.type,
            start_date=data.start_date,
            end_date=data.end_date,
            status=data.status,
        )
        return self.repo.create(db, election_obj)

    def get_election(self, db: Session, election_id: int):
        election = self.repo.get_by_id(db, election_id)
        if not election:
            raise ElectionNotFoundException(election_id)
        return election

    def list_elections(self, db: Session, status: Optional[str] = None):
        if status:
            return self.repo.get_by_status(db, status)
        return self.repo.get_all(db)

    def update_status(self, db: Session, election_id: int, new_status: str):
        """Uses Observer Pattern to notify all registered listeners."""
        election = self.get_election(db, election_id)
        old_status = election.status

        updated = self.repo.update_status(db, election, new_status)

        # Fire observer event
        self._event_manager.status_changed(
            election_id=election.id,
            election_name=election.name,
            old_status=old_status,
            new_status=new_status,
        )
        return updated

    def delete_election(self, db: Session, election_id: int):
        election = self.get_election(db, election_id)
        self.repo.delete(db, election)
        return {"message": f"Election {election_id} deleted"}
