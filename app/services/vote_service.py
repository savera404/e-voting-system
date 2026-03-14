"""
Service Layer – VoteService
Uses:
  - Chain of Responsibility  (vote validation before casting)
  - Strategy Pattern         (vote counting / result calculation)
  - Builder Pattern          (constructing the election result report)
  - Repository Pattern       (VoteRepository, VoterRepository)
"""

from sqlalchemy.orm import Session

from app.repositories.vote_repository import VoteRepository
from app.repositories.voter_repository import VoterRepository
from app.repositories.election_repository import ElectionRepository
from app.models.vote import Vote
from app.models.voter import Voter
from app.patterns.chain.vote_validation_chain import VoteValidationChain, VoteContext
from app.patterns.strategy.vote_counting_strategy import VoteCounter
from app.patterns.builder.report_builder import ElectionResultBuilder
from app.schemas.vote_schema import CastVoteRequest


class VoteService:

    def __init__(self):
        self.vote_repo = VoteRepository()
        self.voter_repo = VoterRepository()
        self.election_repo = ElectionRepository()

    # ── Cast a vote ────────────────────────────────────────────────────────
    def cast_vote(self, db: Session, current_voter: Voter, payload: CastVoteRequest):
        """
        1. Builds the validation chain (Chain of Responsibility).
        2. Runs every check; any failure raises an exception → HTTP 4xx.
        3. Persists the vote and marks the voter as has_voted=True.
        """
        chain = VoteValidationChain.build()
        ctx = VoteContext(
            db=db,
            voter=current_voter,
            candidate_id=payload.candidate_id,
            election_id=payload.election_id,
        )
        chain.handle(ctx)   # raises on failure

        vote = Vote(
            voter_id=current_voter.id,
            candidate_id=payload.candidate_id,
            election_id=payload.election_id,
        )
        saved_vote = self.vote_repo.create(db, vote)
        self.voter_repo.mark_voted(db, current_voter)
        return saved_vote

    # ── Results ────────────────────────────────────────────────────────────
    def get_results(self, db: Session, election_id: int, counting_method: str = "fptp"):
        """
        1. Fetches raw vote counts from the DB.
        2. Applies the chosen Strategy to rank candidates.
        3. Uses Builder to assemble the full report.
        """
        election = self.election_repo.get_by_id(db, election_id)
        if not election:
            from app.core.exceptions import ElectionNotFoundException
            raise ElectionNotFoundException(election_id)

        raw_counts = self.vote_repo.get_vote_counts_for_election(db, election_id)
        total_votes = self.vote_repo.count_for_election(db, election_id)

        # Strategy Pattern: pick counting algorithm
        counter = VoteCounter.for_election_type(counting_method)
        strategy_result = counter.count(raw_counts)

        # Builder Pattern: construct the report
        builder = ElectionResultBuilder()
        builder.set_election(election.id, election.name, election.type or "")
        builder.set_totals(total_votes=total_votes, eligible_voters=total_votes)  # extend with real voter count

        for c in raw_counts:
            builder.add_candidate_result(
                candidate_id=c["candidate_id"],
                name=c["name"],
                party=c["party"],
                votes=c["votes"],
            )

        report = builder.build()

        # Merge strategy-specific fields into the response
        return {
            **strategy_result,
            "election_id": report.election_id,
            "election_name": report.election_name,
            "voter_turnout_percent": report.voter_turnout_percent,
            "generated_at": report.generated_at,
        }
