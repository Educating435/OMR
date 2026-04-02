import logging

from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.models import User, UserRole
from app.repositories.audit_repository import AuditRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse, UserCreate


class AuthService:
    def __init__(self, user_repository: UserRepository, audit_repository: AuditRepository | None = None) -> None:
        self.user_repository = user_repository
        self.audit_repository = audit_repository

    def bootstrap_admin(self, payload: LoginRequest) -> TokenResponse:
        if self.user_repository.get_by_email(payload.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Admin already exists")

        user = User(
            email=payload.email,
            full_name="Administrator",
            hashed_password=hash_password(payload.password),
            role=UserRole.SUPER_ADMIN,
        )
        user = self.user_repository.create(user)
        self._audit(user.id, "bootstrap_admin", "user", user.id, {"role": self._role_value(user)})
        return self._build_token_response(user)

    def login(self, payload: LoginRequest) -> TokenResponse:
        user = self.user_repository.get_by_email(payload.email)
        if user is None or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return self._build_token_response(user)

    def refresh(self, refresh_token: str) -> TokenResponse:
        try:
            claims = jwt.decode(refresh_token, settings.jwt_refresh_secret_key, algorithms=["HS256"])
        except JWTError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from exc
        if claims.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        user = self.user_repository.get(claims["sub"])
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return self._build_token_response(user)

    def create_user(self, payload: UserCreate) -> User:
        if self.user_repository.get_by_email(payload.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
        user = User(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
            role=UserRole(payload.role),
        )
        created = self.user_repository.create(user)
        self._audit(None, "create_user", "user", created.id, {"role": self._role_value(created), "email": created.email})
        return created

    def _build_token_response(self, user: User) -> TokenResponse:
        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
            user_role=self._role_value(user),
        )

    def _role_value(self, user: User) -> str:
        return user.role.value if hasattr(user.role, "value") else str(user.role)

    def _audit(self, actor_user_id: str | None, action: str, entity_type: str, entity_id: str, metadata_json: dict) -> None:
        if self.audit_repository is not None:
            from app.services.audit_service import AuditService

            try:
                AuditService(self.audit_repository).log(actor_user_id, action, entity_type, entity_id, metadata_json)
            except Exception:
                logging.exception("Audit logging failed for action=%s entity_type=%s entity_id=%s", action, entity_type, entity_id)
