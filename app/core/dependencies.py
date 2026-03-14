from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.voter import Voter
from app.models.admin import Admin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/voters/login")

# Admin uses HTTPBearer (shows simple token paste box in Swagger)
bearer_scheme = HTTPBearer()



def get_current_voter(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Voter:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        voter_id: int = payload.get("sub")
        if voter_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    voter = db.query(Voter).filter(Voter.id == int(voter_id)).first()
    if voter is None:
        raise credentials_exception
    return voter


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    db: Session = Depends(get_db),
) -> Admin:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Admin authentication required",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = decode_token(token)
        admin_id = payload.get("sub")
        role = payload.get("role")
        if admin_id is None or role != "admin":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    admin = db.query(Admin).filter(Admin.id == int(admin_id)).first()
    if admin is None:
        raise credentials_exception
    return admin