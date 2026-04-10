# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Auth Middleware
#  File: backend/api/middleware/auth_middleware.py
# ============================================================

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from core.security import decode_access_token
from core.logging import logger


# ----------------------------------------------------------
# DAFTAR PATH YANG TIDAK PERLU TOKEN (public)
# ----------------------------------------------------------
PUBLIC_PATHS = [
    "/",
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/api/auth/login",
    "/api/auth/register",
]


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware untuk memvalidasi JWT token di setiap request.
    Path yang ada di PUBLIC_PATHS bebas diakses tanpa token.
    """

    async def dispatch(self, request: Request, call_next) -> Response:

        # Lewati validasi untuk public path
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        # Ambil token dari header Authorization
        authorization: str = request.headers.get("Authorization", "")

        if not authorization.startswith("Bearer "):
            logger.warning(f"Request tanpa token: {request.url.path}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token tidak ditemukan",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = authorization.split(" ")[1]
        payload = decode_access_token(token)

        if payload is None:
            logger.warning(f"Token tidak valid: {request.url.path}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token tidak valid atau sudah kedaluwarsa",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Simpan user_id di request state agar bisa diakses di route
        request.state.user_id = int(payload.get("sub", 0))

        return await call_next(request)