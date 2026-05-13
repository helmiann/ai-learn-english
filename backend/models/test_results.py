# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Test Results Model
#  File: backend/models/test_results.py
# ============================================================

from datetime import datetime, timezone
from sqlalchemy import Integer, JSON, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class TestResult(Base):
    __tablename__ = "test_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_user: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id_user", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    test_type: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        # Nilai: "pre" atau "post"
    )

    # Nilai total
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    correct: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[int] = mapped_column(Integer, nullable=False)

    # Nilai per materi (dari 5, karena 5 soal per materi)
    score_simple_present: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    score_simple_past: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    score_irregular_verbs: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    score_imperative: Mapped[int] = mapped_column(Integer, nullable=True, default=0)

    # Jawaban lengkap dalam JSON
    answers: Mapped[dict] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<TestResult user={self.id_user} type={self.test_type} score={self.score}>"