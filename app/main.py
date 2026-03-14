from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import engine, Base
from app.models import *

from app.routes import voter_router, admin_router, candidate_router,election_router,location_router,vote_router


from app.core.exceptions import (
    VoterNotFoundException, voter_not_found_handler,
    ElectionNotFoundException, election_not_found_handler,
    AlreadyVotedException, already_voted_handler,
    ElectionNotActiveException, election_not_active_handler,
    ConstituencyMismatchException, constituency_mismatch_handler,
    DuplicateEntryException, duplicate_entry_handler,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Voting System",
    version="1.0.0",
)
# ── Exception Handlers ─────────────────────────────────────────────────────
app.add_exception_handler(VoterNotFoundException, voter_not_found_handler)
app.add_exception_handler(ElectionNotFoundException, election_not_found_handler)
app.add_exception_handler(AlreadyVotedException, already_voted_handler)
app.add_exception_handler(ElectionNotActiveException, election_not_active_handler)
app.add_exception_handler(ConstituencyMismatchException, constituency_mismatch_handler)
app.add_exception_handler(DuplicateEntryException, duplicate_entry_handler)

@app.get("/")
def root():
    return {"message": "E-Voting Backend Running Successfully"}


@app.get("/check_db_connection")
def check_db_connection():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        return {"database_connection": "successful"}

app.include_router(admin_router.router,     prefix="/admins",      tags=["Admins"])
app.include_router(voter_router.router,     prefix="/voters",        tags=["Voters"])
app.include_router(candidate_router.router, prefix="/candidates",    tags=["Candidates"])
app.include_router(election_router.router,  prefix="/elections",     tags=["Elections"])
app.include_router(location_router.router,  prefix="/locations",     tags=["Locations"])
app.include_router(vote_router.router,      prefix="/votes",         tags=["Votes"])