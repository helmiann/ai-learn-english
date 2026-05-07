# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Test & Survey Schemas
#  File: backend/schemas/test.py
# ============================================================

from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel


# ----------------------------------------------------------
# TEST REQUEST & RESPONSE
# ----------------------------------------------------------
class SectionScores(BaseModel):
    """Nilai per materi."""
    simple_present: int = 0
    simple_past: int = 0
    irregular_verbs: int = 0
    imperative: int = 0


class TestSubmit(BaseModel):
    """Schema untuk submit hasil pre-test atau post-test."""
    answers: Dict[int, str]
    score: int
    correct: int
    total: int
    section_scores: SectionScores  # ← nilai per materi


class TestResultResponse(BaseModel):
    """Schema untuk menampilkan hasil test."""
    id: int
    test_type: str
    score: int
    correct: int
    total: int
    score_simple_present: int = 0
    score_simple_past: int = 0
    score_irregular_verbs: int = 0
    score_imperative: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class TestCheckResponse(BaseModel):
    """Schema untuk cek apakah sudah pernah test."""
    already_taken: bool
    score: Optional[int] = None


# ----------------------------------------------------------
# SURVEY REQUEST & RESPONSE
# ----------------------------------------------------------
class SurveySubmit(BaseModel):
    """Schema untuk submit hasil kuesioner."""
    answers: Dict[int, int]
    saran: Optional[str] = ""
    avg_context: float
    avg_usability: float
    avg_learning: float
    avg_total: float


class SurveyResultResponse(BaseModel):
    """Schema untuk menampilkan hasil kuesioner."""
    id: int
    avg_context: float
    avg_usability: float
    avg_learning: float
    avg_total: float
    saran: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}