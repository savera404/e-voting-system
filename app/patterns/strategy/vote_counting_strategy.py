"""
Design Pattern #7: Strategy Pattern
──────────────────────────────────────
Different elections may want different vote-counting / result-ranking rules.
The Strategy pattern lets the service layer swap algorithms at runtime without
changing any calling code.

Strategies provided
--------------------
* FirstPastThePostStrategy   – candidate with most votes wins (FPTP / plurality)
* ProportionalStrategy       – ranks by vote share percentage
* RunoffStrategy             – if no candidate has >50 %, top-2 are flagged for runoff

Usage
-----
    counter = VoteCounter(FirstPastThePostStrategy())
    result  = counter.count(votes_data)
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Any


# ── Input type ─────────────────────────────────────────────────────────────

CandidateVotes = List[Dict[str, Any]]
# Each dict: {"candidate_id": int, "name": str, "party": str, "votes": int}


# ── Abstract Strategy ──────────────────────────────────────────────────────

class VoteCountingStrategy(ABC):
    @abstractmethod
    def count(self, data: CandidateVotes) -> Dict[str, Any]:
        """
        Processes raw vote counts and returns a structured result dict.
        Must include at minimum: 'ranked_candidates' and 'winner' keys.
        """


# ── Concrete Strategies ────────────────────────────────────────────────────

class FirstPastThePostStrategy(VoteCountingStrategy):
    """
    FPTP / Plurality: the candidate with the highest vote count wins outright.
    Used in Pakistani general elections (National Assembly, Provincial Assemblies).
    """

    def count(self, data: CandidateVotes) -> Dict[str, Any]:
        if not data:
            return {"method": "fptp", "winner": None, "ranked_candidates": []}

        total = sum(d["votes"] for d in data)
        ranked = sorted(data, key=lambda x: x["votes"], reverse=True)

        for c in ranked:
            c["percentage"] = round(c["votes"] / total * 100, 2) if total else 0

        return {
            "method": "fptp",
            "total_votes": total,
            "winner": ranked[0],
            "ranked_candidates": ranked,
        }


class ProportionalStrategy(VoteCountingStrategy):
    """
    Proportional Representation: seats/ranking assigned based on vote share.
    Could be used for party-list elections.
    """

    def count(self, data: CandidateVotes) -> Dict[str, Any]:
        if not data:
            return {"method": "proportional", "winner": None, "ranked_candidates": []}

        total = sum(d["votes"] for d in data)
        ranked = sorted(data, key=lambda x: x["votes"], reverse=True)

        for c in ranked:
            c["vote_share"] = round(c["votes"] / total * 100, 2) if total else 0

        return {
            "method": "proportional",
            "total_votes": total,
            "winner": ranked[0],        # party/candidate with highest share
            "ranked_candidates": ranked,
        }


class RunoffStrategy(VoteCountingStrategy):
    """
    Two-round runoff: if no candidate exceeds 50 %, the top two proceed
    to a second round.  Returns a 'requires_runoff' flag the service can act on.
    """

    MAJORITY_THRESHOLD = 50.0

    def count(self, data: CandidateVotes) -> Dict[str, Any]:
        if not data:
            return {"method": "runoff", "winner": None, "ranked_candidates": []}

        total = sum(d["votes"] for d in data)
        ranked = sorted(data, key=lambda x: x["votes"], reverse=True)

        for c in ranked:
            c["percentage"] = round(c["votes"] / total * 100, 2) if total else 0

        top = ranked[0]
        requires_runoff = top["percentage"] < self.MAJORITY_THRESHOLD

        return {
            "method": "runoff",
            "total_votes": total,
            "requires_runoff": requires_runoff,
            "runoff_candidates": ranked[:2] if requires_runoff else [],
            "winner": None if requires_runoff else top,
            "ranked_candidates": ranked,
        }


# ── Context (Strategy holder) ──────────────────────────────────────────────

class VoteCounter:
    """
    The context that the service layer interacts with.
    Swap the strategy without changing any service code.
    """

    _STRATEGY_MAP = {
        "fptp":         FirstPastThePostStrategy,
        "proportional": ProportionalStrategy,
        "runoff":       RunoffStrategy,
    }

    def __init__(self, strategy: VoteCountingStrategy | None = None) -> None:
        self._strategy = strategy or FirstPastThePostStrategy()

    @classmethod
    def for_election_type(cls, election_type: str) -> "VoteCounter":
        """Factory helper: pick default strategy based on election type."""
        strategy_cls = cls._STRATEGY_MAP.get(election_type, FirstPastThePostStrategy)
        return cls(strategy_cls())

    def set_strategy(self, strategy: VoteCountingStrategy) -> None:
        self._strategy = strategy

    def count(self, data: CandidateVotes) -> Dict[str, Any]:
        return self._strategy.count(data)
