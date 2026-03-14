"""
Design Pattern #6: Chain of Responsibility
────────────────────────────────────────────
Before a vote is cast, it must pass a pipeline of validation checks.
Each handler in the chain either passes the request to the next handler
or raises an exception that aborts the chain.

Handlers (in order)
--------------------
1. ElectionActiveHandler       – Is the election currently active?
2. VoterEligibilityHandler     – Has the voter already cast a vote?
3. ConstituencyMatchHandler    – Does the voter's constituency match the candidate's?
4. CandidateExistsHandler      – Does the chosen candidate belong to this election?

Usage
-----
    chain = VoteValidationChain.build()
    chain.handle(context)   # raises an app exception on failure, returns None on pass
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.orm import Session

from app.core.exceptions import (
    ElectionNotActiveException,
    AlreadyVotedException,
    ConstituencyMismatchException,
    ElectionNotFoundException,
)
from app.models.election import Election
from app.models.voter import Voter
from app.models.candidate import Candidate


# ── Request context ────────────────────────────────────────────────────────
#This is just a container that carries all the information the chain needs. Instead of passing 4+ separate arguments to every handler, you pack everything into one VoteContext object and pass that down the chain.

class VoteContext:
    """Carries everything the handlers need; passed down the chain."""

    def __init__(
        self,
        db: Session,
        voter: Voter,
        candidate_id: int,
        election_id: int,
    ) -> None:
        self.db = db
        self.voter = voter
        self.candidate_id = candidate_id
        self.election_id = election_id

        # Populated lazily by handlers so we avoid redundant DB queries
        self.election: Optional[Election] = None
        self.candidate: Optional[Candidate] = None


# ── Abstract Handler ───────────────────────────────────────────────────────


"""
Every handler in the chain inherits from this. The key method is handle():

First runs its own check()
If check passes → calls the next handler's handle()
If check fails → throws an exception, chain stops

set_next() returns the handler you just set, which allows neat chaining syntax when building the chain.
"""
class VoteHandler(ABC):
    def __init__(self) -> None:
        self._next: Optional["VoteHandler"] = None

    def set_next(self, handler: "VoteHandler") -> "VoteHandler":
        self._next = handler
        return handler   # allows chaining: a.set_next(b).set_next(c)

    def handle(self, ctx: VoteContext) -> None:
        self.check(ctx)
        if self._next:
            self._next.handle(ctx)

    @abstractmethod
    def check(self, ctx: VoteContext) -> None:
        """Raise an appropriate exception if the check fails."""


# ── Concrete Handlers ──────────────────────────────────────────────────────

class ElectionExistsHandler(VoteHandler):
    def check(self, ctx: VoteContext) -> None:
        election = ctx.db.query(Election).filter(Election.id == ctx.election_id).first()
        if election is None:
            raise ElectionNotFoundException(ctx.election_id)
        ctx.election = election   # cache for downstream handlers


class ElectionActiveHandler(VoteHandler):
    def check(self, ctx: VoteContext) -> None:
        if ctx.election.status != "active":
            raise ElectionNotActiveException(ctx.election_id, ctx.election.status)


class VoterEligibilityHandler(VoteHandler):
    def check(self, ctx: VoteContext) -> None:
        if ctx.voter.has_voted:
            raise AlreadyVotedException(ctx.voter.id, ctx.election_id)


class CandidateExistsHandler(VoteHandler):
    def check(self, ctx: VoteContext) -> None:
        candidate = (
            ctx.db.query(Candidate)
            .filter(Candidate.id == ctx.candidate_id)
            .first()
        )
        if candidate is None:
            from app.core.exceptions import VoterNotFoundException  # reuse 404
            raise ValueError(f"Candidate {ctx.candidate_id} not found")
        ctx.candidate = candidate


class ConstituencyMatchHandler(VoteHandler):
    def check(self, ctx: VoteContext) -> None:
        if ctx.voter.constituency_id != ctx.candidate.constituency_id:
            raise ConstituencyMismatchException(ctx.voter.id, ctx.candidate_id)


# ── Chain Builder ──────────────────────────────────────────────────────────



class VoteValidationChain:
    """Assembles and returns the head of the validation chain."""

    @staticmethod
    def build() -> VoteHandler:
        head = ElectionExistsHandler()
        head \
            .set_next(ElectionActiveHandler()) \
            .set_next(VoterEligibilityHandler()) \
            .set_next(CandidateExistsHandler()) \
            .set_next(ConstituencyMatchHandler())
        return head
