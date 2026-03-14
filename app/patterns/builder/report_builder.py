"""
Design Pattern #7: Builder Pattern
────────────────────────────────────
Building an election result report requires assembling multiple pieces
of information: election details, vote totals, per-candidate results,
and turnout percentage. The Builder pattern lets us construct this
complex object step by step instead of passing everything to one
giant constructor.

Usage
-----
    builder = ElectionResultBuilder()
    builder.set_election(election.id, election.name, election.type)
    builder.set_totals(total_votes=500, eligible_voters=1000)
    builder.add_candidate_result(candidate_id=1, name="Ahmed", party="PTI", votes=300)
    builder.add_candidate_result(candidate_id=2, name="Ali",   party="PMLN", votes=200)
    report = builder.build()
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional


# ── Product ────────────────────────────────────────────────────────────────

@dataclass
class ElectionResultReport:
    """The final object produced by the builder."""

    election_id: int
    election_name: str
    election_type: str
    total_votes: int
    eligible_voters: int
    voter_turnout_percent: float
    candidate_results: List[dict]
    generated_at: str


# ── Builder ────────────────────────────────────────────────────────────────

class ElectionResultBuilder:
    """
    Assembles an ElectionResultReport piece by piece.
    Call build() at the end to get the final report object.
    """

    def __init__(self) -> None:
        self._reset()

    def _reset(self) -> None:
        """Clears internal state so the builder can be reused."""
        self._election_id: Optional[int] = None
        self._election_name: str = ""
        self._election_type: str = ""
        self._total_votes: int = 0
        self._eligible_voters: int = 0
        self._candidate_results: List[dict] = []

    # ── Step 1 ─────────────────────────────────────────────────────────────
    def set_election(
        self,
        election_id: int,
        election_name: str,
        election_type: str,
    ) -> "ElectionResultBuilder":
        self._election_id = election_id
        self._election_name = election_name
        self._election_type = election_type
        return self   # allows method chaining

    # ── Step 2 ─────────────────────────────────────────────────────────────
    def set_totals(
        self,
        total_votes: int,
        eligible_voters: int,
    ) -> "ElectionResultBuilder":
        self._total_votes = total_votes
        self._eligible_voters = eligible_voters
        return self

    # ── Step 3 (repeat for each candidate) ────────────────────────────────
    def add_candidate_result(
        self,
        candidate_id: int,
        name: str,
        party: str,
        votes: int,
    ) -> "ElectionResultBuilder":
        percentage = (
            round(votes / self._total_votes * 100, 2)
            if self._total_votes > 0 else 0.0
        )
        self._candidate_results.append({
            "candidate_id": candidate_id,
            "name": name,
            "party": party,
            "votes": votes,
            "percentage": percentage,
        })
        return self

    # ── Final step ─────────────────────────────────────────────────────────
    def build(self) -> ElectionResultReport:
        """Validates and returns the completed report."""
        if self._election_id is None:
            raise ValueError("Cannot build report: election details not set. Call set_election() first.")

        turnout = (
            round(self._total_votes / self._eligible_voters * 100, 2)
            if self._eligible_voters > 0 else 0.0
        )

        report = ElectionResultReport(
            election_id=self._election_id,
            election_name=self._election_name,
            election_type=self._election_type,
            total_votes=self._total_votes,
            eligible_voters=self._eligible_voters,
            voter_turnout_percent=turnout,
            candidate_results=self._candidate_results,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

        self._reset()   # ready for reuse
        return report