from sqlalchemy.orm import Session

from app.models.audit import AuditLog


class AuditLogService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def log(
        self,
        *,
        actor_user_id: str | None,
        action: str,
        entity_type: str,
        entity_id: str,
        description: str,
        payload: dict | None = None,
    ) -> None:
        entry = AuditLog(
            actor_user_id=actor_user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            payload=payload or {},
        )
        self.db.add(entry)
