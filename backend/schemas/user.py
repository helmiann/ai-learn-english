# ============================================================
#  ENGLISH GRAMMAR CHATBOT — User Schemas
#  File: backend/schemas/user.py
# ============================================================

from pydantic import BaseModel, field_validator


# ----------------------------------------------------------
# REQUEST — Data yang diterima dari frontend
# ----------------------------------------------------------
class UserCreate(BaseModel):
    """Schema untuk register akun baru."""

    username: str
    password: str

    @field_validator("username")
    @classmethod
    def username_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username minimal 3 karakter")
        if len(v) > 50:
            raise ValueError("Username maksimal 50 karakter")
        if not v.isalnum() and "_" not in v:
            raise ValueError("Username hanya boleh huruf, angka, dan underscore")
        return v

    @field_validator("password")
    @classmethod
    def password_valid(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password minimal 6 karakter")
        return v


# ----------------------------------------------------------
# RESPONSE — Data yang dikirim ke frontend
# ----------------------------------------------------------
class UserResponse(BaseModel):
    """Schema untuk menampilkan data user (tanpa password)."""

    id_user: int
    username: str

    model_config = {"from_attributes": True}


# ----------------------------------------------------------
# TOKEN RESPONSE — Hasil login
# ----------------------------------------------------------
class TokenResponse(BaseModel):
    """Schema untuk response login yang berisi JWT token."""

    access_token: str
    token_type: str = "bearer"