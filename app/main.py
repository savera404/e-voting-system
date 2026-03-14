from fastapi import FastAPI
from app.core.database import engine
from sqlalchemy import text
from app.core.database import engine, Base
from app.models import *
from app.routes import voter_router

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def root():
    return {"message": "E-Voting Backend Running Successfully"}

@app.get("/check_db_connection")
def root():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"database_connection": "successful"}
    
app.include_router(voter_router.router, prefix="/voters", tags=["Voters"])