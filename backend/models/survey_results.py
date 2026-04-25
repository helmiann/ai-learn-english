# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Survey Results Model
#  File: backend/models/survey_results.py
#  Tabel: survey_results
# ============================================================

from datetime import datetime, timezone
from sqlalchemy import Integer, String, Float, Text, JSON, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class SurveyResult(Base):
    __tablename__ = "survey_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_user: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id_user", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    answers: Mapped[dict] = mapped_column(JSON, nullable=False)
    saran: Mapped[str] = mapped_column(Text, nullable=True)
    avg_context: Mapped[float] = mapped_column(Float, nullable=False)
    avg_usability: Mapped[float] = mapped_column(Float, nullable=False)
    avg_learning: Mapped[float] = mapped_column(Float, nullable=False)
    avg_total: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<SurveyResult user={self.id_user} avg={self.avg_total}>"