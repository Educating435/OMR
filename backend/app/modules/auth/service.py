from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.security.hashing import verify_password
from app.security.jwt import create_access_token


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def login(self, email: str, password: str) -> tuple[User, str]:
        user = self.db.scalar(select(User).where(User.email == email))
        if user is None or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        return user, create_access_token(user.id, user.role)
