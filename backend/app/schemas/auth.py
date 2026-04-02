from pydantic import EmailStr

from app.schemas.common import ORMModel


class LoginRequest(ORMModel):
    email: EmailStr
    password: str


class TokenResponse(ORMModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_role: str


class UserRead(ORMModel):
    id: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool


class RefreshRequest(ORMModel):
    refresh_token: str


class UserCreate(ORMModel):
    email: EmailStr
    password: str
    full_name: str
    role: str
