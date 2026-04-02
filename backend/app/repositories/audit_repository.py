from app.models import AuditLog
from sqlalchemy.orm import Session


class AuditRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, item: AuditLog) -> AuditLog:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
