from fastapi import APIRouter

from app.schemas import VisualAnalysisReport
from app.services.report_service import generate_mock_report

router = APIRouter()


@router.post("/analyze")
def analyze() -> VisualAnalysisReport:
    return generate_mock_report()
