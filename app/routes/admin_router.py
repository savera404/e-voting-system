from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.admin_schema import AdminCreate, AdminLogin
from app.services.admin_service import AdminService
from app.core.database import get_db

router = APIRouter()
service = AdminService()


@router.post("/register")
def register_admin(data: AdminCreate, db: Session = Depends(get_db)):
    return service.register_admin(db, data)


@router.post("/login")
def login_admin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    credentials = AdminLogin(email=form_data.username, password=form_data.password)
    return service.login_admin(db, credentials)