# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Test & Survey Routes
#  File: backend/api/routes/test.py
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.database import get_db
from core.security import get_current_user_id
from core.logging import logger
from models.test_results import TestResult
from models.survey_results import SurveyResult
from schemas.test import (
    TestSubmit,
    TestResultResponse,
    TestCheckResponse,
    SurveySubmit,
    SurveyResultResponse,
)

router = APIRouter()


# ----------------------------------------------------------
# POST /api/test/pre-test
# ----------------------------------------------------------
@router.post(
    "/pre-test",
    response_model=TestResultResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Simpan hasil pre-test",
)
async def submit_pre_test(
    data: TestSubmit,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    # Cek apakah sudah pernah pre-test
    existing = await db.execute(
        select(TestResult).where(
            TestResult.id_user == user_id,
            TestResult.test_type == "pre",
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kamu sudah mengerjakan pre-test",
        )

    result = TestResult(
        id_user=user_id,
        test_type="pre",
        score=data.score,
        correct=data.correct,
        total=data.total,
        score_simple_present=data.section_scores.simple_present,
        score_simple_past=data.section_scores.simple_past,
        score_irregular_verbs=data.section_scores.irregular_verbs,
        score_imperative=data.section_scores.imperative,
        answers=data.answers,
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)

    logger.info(f"Pre-test disimpan: user={user_id} score={data.score}")
    return result


# ----------------------------------------------------------
# GET /api/test/pre-test/check
# ----------------------------------------------------------
@router.get(
    "/pre-test/check",
    response_model=TestCheckResponse,
    summary="Cek status pre-test",
)
async def check_pre_test(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TestResult).where(
            TestResult.id_user == user_id,
            TestResult.test_type == "pre",
        )
    )
    existing = result.scalar_one_or_none()
    return TestCheckResponse(
        already_taken=existing is not None,
        score=existing.score if existing else None,
    )


# ----------------------------------------------------------
# GET /api/test/pre-test/result
# ----------------------------------------------------------
@router.get(
    "/pre-test/result",
    response_model=TestResultResponse,
    summary="Ambil hasil pre-test",
)
async def get_pre_test_result(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TestResult).where(
            TestResult.id_user == user_id,
            TestResult.test_type == "pre",
        )
    )
    existing = result.scalar_one_or_none()
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pre-test belum dikerjakan",
        )
    return existing


# ----------------------------------------------------------
# POST /api/test/post-test
# ----------------------------------------------------------
@router.post(
    "/post-test",
    response_model=TestResultResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Simpan hasil post-test",
)
async def submit_post_test(
    data: TestSubmit,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = TestResult(
        id_user=user_id,
        test_type="post",
        score=data.score,
        correct=data.correct,
        total=data.total,
        score_simple_present=data.section_scores.simple_present,
        score_simple_past=data.section_scores.simple_past,
        score_irregular_verbs=data.section_scores.irregular_verbs,
        score_imperative=data.section_scores.imperative,
        answers=data.answers,
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)

    logger.info(f"Post-test disimpan: user={user_id} score={data.score}")
    return result


# ----------------------------------------------------------
# POST /api/survey/submit (dipakai dengan prefix /api/survey)
# ----------------------------------------------------------
@router.post(
    "/submit",
    response_model=SurveyResultResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Simpan hasil kuesioner",
)
async def submit_survey(
    data: SurveySubmit,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    survey = SurveyResult(
        id_user=user_id,
        answers=data.answers,
        saran=data.saran,
        avg_context=data.avg_context,
        avg_usability=data.avg_usability,
        avg_learning=data.avg_learning,
        avg_total=data.avg_total,
    )
    db.add(survey)
    await db.commit()
    await db.refresh(survey)

    logger.info(f"Kuesioner disimpan: user={user_id} avg={data.avg_total}")
    return survey