from fastapi import Request
from fastapi.responses import JSONResponse


# ──────────────────────────────────────────────
# Custom exception classes
# ──────────────────────────────────────────────

class VoterNotFoundException(Exception):
    def __init__(self, voter_id: int):
        self.voter_id = voter_id
        super().__init__(f"Voter {voter_id} not found")


class ElectionNotFoundException(Exception):
    def __init__(self, election_id: int):
        self.election_id = election_id
        super().__init__(f"Election {election_id} not found")


class AlreadyVotedException(Exception):
    def __init__(self, voter_id: int, election_id: int):
        self.voter_id = voter_id
        self.election_id = election_id
        super().__init__(f"Voter {voter_id} already voted in election {election_id}")


class ElectionNotActiveException(Exception):
    def __init__(self, election_id: int, current_status: str):
        self.election_id = election_id
        self.current_status = current_status
        super().__init__(f"Election {election_id} is not active (status={current_status})")


class ConstituencyMismatchException(Exception):
    def __init__(self, voter_id: int, candidate_id: int):
        self.voter_id = voter_id
        self.candidate_id = candidate_id
        super().__init__(
            f"Voter {voter_id} cannot vote for candidate {candidate_id} — constituency mismatch"
        )


class DuplicateEntryException(Exception):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"{field} '{value}' is already registered")


# ──────────────────────────────────────────────
# FastAPI exception handlers
# ──────────────────────────────────────────────

async def voter_not_found_handler(request: Request, exc: VoterNotFoundException):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


async def election_not_found_handler(request: Request, exc: ElectionNotFoundException):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


async def already_voted_handler(request: Request, exc: AlreadyVotedException):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


async def election_not_active_handler(request: Request, exc: ElectionNotActiveException):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


async def constituency_mismatch_handler(request: Request, exc: ConstituencyMismatchException):
    return JSONResponse(status_code=403, content={"detail": str(exc)})


async def duplicate_entry_handler(request: Request, exc: DuplicateEntryException):
    return JSONResponse(status_code=409, content={"detail": str(exc)})
