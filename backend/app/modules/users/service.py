from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.modules.audit_logs.service import AuditLogService
from app.modules.users.schemas import UserCreate
from app.security.hashing import hash_password


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.audit = AuditLogService(db)

    def list_users(self) -> list[User]:
        return list(self.db.scalars(select(User).order_by(User.created_at.desc())))

    def create_user(self, payload: UserCreate, actor_id: str | None) -> User:
        user = User(
            full_name=payload.full_name,
            email=payload.email,
            password_hash=hash_password(payload.password),
            role=payload.role,
        )
        self.db.add(user)
        self.db.flush()
        self.audit.log(
            actor_user_id=actor_id,
            action="user.created",
            entity_type="user",
            entity_id=user.id,
            description=f"Created user {user.email}",
        )
        self.db.commit()
        self.db.refresh(user)
        return user
