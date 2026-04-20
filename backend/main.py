# ============================================================
#  ENGLISH GRAMMAR CHATBOT — FastAPI Entry Point
#  File: backend/main.py
# ============================================================

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from core.config import settings
from core.logging import setup_logging
from db.database import init_db
from api.routes import auth, chat, history
from infrastructure.redis_client import init_redis, close_redis
from services.grammar_checker.grammar_checker_service import grammar_checker


# ----------------------------------------------------------
# LIFESPAN — Jalankan saat startup & shutdown
# ----------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    setup_logging()
    await init_db()
    await init_redis()
    #grammar_checker.initialize()

    yield

    # --- Shutdown ---
    await close_redis()
    grammar_checker.close()


# ----------------------------------------------------------
# INISIALISASI APLIKASI
# ----------------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    description="API Chatbot untuk belajar Grammar Bahasa Inggris bagi Siswa SMP",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# ----------------------------------------------------------
# MIDDLEWARE
# ----------------------------------------------------------

# CORS — izinkan frontend mengakses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host — keamanan tambahan
if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1"],
    )


# ----------------------------------------------------------
# ROUTES
# ----------------------------------------------------------
app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Authentication"],
)

app.include_router(
    chat.router,
    prefix="/api/chat",
    tags=["Chat"],
)

app.include_router(
    history.router,
    prefix="/api/history",
    tags=["History"],
)


# ----------------------------------------------------------
# ROOT ENDPOINT
# ----------------------------------------------------------
@app.get("/", tags=["Root"])
async def root():
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}