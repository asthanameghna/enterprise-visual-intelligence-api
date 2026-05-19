from fastapi import APIRouter, HTTPException

from app.schemas import VisualAnalysisReport
from app.services.storage_service import load_report

router = APIRouter()


@router.get("/reports/{report_id}", response_model=VisualAnalysisReport)
def get_report(report_id: str):
    try:
        return load_report(report_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Report not found")
