from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.voter import Voter

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/voters/login")

#This is a FastAPI dependency that gets injected into any route that requires a logged-in voter. It does 3 things in order

def get_current_voter(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Voter:
    """
    FastAPI dependency injected into any route that requires authentication.
    Decodes the JWT, looks up the voter, and returns the ORM object.
    Raises 401 on any failure so callers never receive a None voter.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    #Step 1 — Decode the token:
    try:
        payload = decode_token(token)
        voter_id: int = payload.get("sub")
        #Step 2 — Validate the token:
        if voter_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    #Step 3 — Look up the voter in DB:
    voter = db.query(Voter).filter(Voter.id == int(voter_id)).first()
    if voter is None:
        raise credentials_exception

    return voter
