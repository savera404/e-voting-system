"""
Service Layer – VoterService
Uses: Repository Pattern, Singleton (via config/security)
"""

from sqlalchemy.orm import Session

from app.repositories.voter_repository import VoterRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import DuplicateEntryException, VoterNotFoundException
from app.schemas.voter_schema import VoterCreate, VoterLogin, TokenResponse


class VoterService:

    def __init__(self):
        self.repo = VoterRepository()

    def register_voter(self, db: Session, voter_data: VoterCreate):
        if self.repo.get_by_email(db, voter_data.email):
            raise DuplicateEntryException("email", voter_data.email)
        if self.repo.get_by_cnic(db, voter_data.cnic):
            raise DuplicateEntryException("CNIC", voter_data.cnic)

        # Hash password before storing
        data = voter_data.model_copy(update={"password": hash_password(voter_data.password)})
        return self.repo.create_voter(db, data)

    def login_voter(self, db: Session, credentials: VoterLogin) -> TokenResponse:
        voter = self.repo.get_by_email(db, credentials.email)
        if not voter or not verify_password(credentials.password, voter.password):
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        token = create_access_token(data={"sub": str(voter.id)})
        return TokenResponse(access_token=token, voter_id=voter.id, name=voter.name)

    def get_voter(self, db: Session, voter_id: int):
        voter = self.repo.get_by_id(db, voter_id)
        if not voter:
            raise VoterNotFoundException(voter_id)
        return voter

    def list_voters(self, db: Session, skip: int = 0, limit: int = 100):
        return self.repo.get_all(db, skip, limit)
