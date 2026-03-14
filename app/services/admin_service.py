from sqlalchemy.orm import Session
from app.repositories.admin_repository import AdminRepository
from app.models.admin import Admin
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.admin_schema import AdminCreate, AdminLogin, AdminTokenResponse
from fastapi import HTTPException, status


class AdminService:

    def __init__(self):
        self.repo = AdminRepository()

    def register_admin(self, db: Session, data: AdminCreate) -> Admin:
        if self.repo.get_by_email(db, data.email):
            raise HTTPException(status_code=409, detail="Email already registered")
        admin = Admin(
            name=data.name,
            email=data.email,
            password=hash_password(data.password),
        )
        return self.repo.create(db, admin)

    def login_admin(self, db: Session, credentials: AdminLogin) -> AdminTokenResponse:
        admin = self.repo.get_by_email(db, credentials.email)
        if not admin or not verify_password(credentials.password, admin.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        token = create_access_token(data={"sub": str(admin.id), "role": "admin"})
        return AdminTokenResponse(
            access_token=token,
            admin_id=admin.id,
            name=admin.name,
        )