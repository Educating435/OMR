from app.models import AuditLog
from app.repositories.audit_repository import AuditRepository


class AuditService:
    def __init__(self, repository: AuditRepository) -> None:
        self.repository = repository

    def log(self, actor_user_id: str | None, action: str, entity_type: str, entity_id: str, metadata_json: dict | None = None) -> None:
        self.repository.create(
            AuditLog(
                actor_user_id=actor_user_id,
                action=action,
                entity_type=entity_type,
                entity_id=entity_id,
                metadata_json=metadata_json or {},
            )
        )
