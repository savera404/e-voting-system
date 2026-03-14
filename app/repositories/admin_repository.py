from typing import Optional
from sqlalchemy.orm import Session
from app.models.admin import Admin


class AdminRepository:

    def create(self, db: Session, admin: Admin) -> Admin:
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return admin

    def get_by_email(self, db: Session, email: str) -> Optional[Admin]:
        return db.query(Admin).filter(Admin.email == email).first()

    def get_by_id(self, db: Session, admin_id: int) -> Optional[Admin]:
        return db.query(Admin).filter(Admin.id == admin_id).first()