from fastapi import APIRouter, HTTPException

from app.schemas import VisualAnalysisReport
from app.services.db_storage_service import load_report_from_db

router = APIRouter()


@router.get("/reports/{report_id}", response_model=VisualAnalysisReport)
def get_report(report_id: str):
    report = load_report_from_db(report_id)

    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    return report
