# ============================================================
#  ENGLISH GRAMMAR CHATBOT — User Schemas
#  File: backend/schemas/user.py
# ============================================================

from typing import Optional
from pydantic import BaseModel, field_validator


class UserCreate(BaseModel):
    """Schema untuk register akun baru."""
    username: str
    password: str
    kelas: str
    sekolah: str

    @field_validator("username")
    @classmethod
    def username_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username minimal 3 karakter")
        if len(v) > 50:
            raise ValueError("Username maksimal 50 karakter")
        return v

    @field_validator("password")
    @classmethod
    def password_valid(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password minimal 6 karakter")
        return v

    @field_validator("kelas")
    @classmethod
    def kelas_valid(cls, v: str) -> str:
        v = v.strip()
        mapping = {"7": "VII", "8": "VIII", "9": "IX"}
        return mapping.get(v, v)

    @field_validator("sekolah")
    @classmethod
    def sekolah_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Nama sekolah minimal 3 karakter")
        return v


class UserResponse(BaseModel):
    """Schema untuk menampilkan data user (tanpa password)."""
    id_user: int
    username: str
    kelas: Optional[str] = None
    sekolah: Optional[str] = None

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """Schema untuk response login."""
    access_token: str
    token_type: str = "bearer"