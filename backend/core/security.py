# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Security & Auth Helper
#  File: backend/core/security.py
# ============================================================

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.config import settings


# ----------------------------------------------------------
# PASSWORD HASHING
# ----------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash password menggunakan bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifikasi password plain dengan hash yang tersimpan di database."""
    return pwd_context.verify(plain_password, hashed_password)


# ----------------------------------------------------------
# JWT TOKEN
# ----------------------------------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Buat JWT access token.
    - data: payload yang ingin disimpan di token (biasanya {"sub": user_id})
    - expires_delta: durasi kedaluwarsa, default dari settings
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode dan validasi JWT token.
    Return payload dict jika valid, None jika tidak valid.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        return None


# ----------------------------------------------------------
# DEPENDENCY — Dipakai di route yang butuh login
# ----------------------------------------------------------
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """
    FastAPI dependency untuk mendapatkan user_id dari token.
    Gunakan sebagai parameter di route: user_id: int = Depends(get_current_user_id)
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token tidak valid atau sudah kedaluwarsa",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)

    if payload is None:
        raise credentials_exception

    user_id: Optional[str] = payload.get("sub")

    if user_id is None:
        raise credentials_exception

    return int(user_id)