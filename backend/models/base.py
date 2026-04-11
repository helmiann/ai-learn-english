# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Base Model
#  File: backend/models/base.py
# ============================================================

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class untuk semua model SQLAlchemy.
    Semua model harus inherit dari class ini.
    """
    pass