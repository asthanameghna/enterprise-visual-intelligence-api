from fastapi import APIRouter, File, UploadFile

from app.services import report_service
from app.utils.image_utils import validate_image_file

router = APIRouter()


@router.post("/analyze")
def analyze(file: UploadFile = File(...)):
    validate_image_file(file)
    return report_service.generate_mock_report()
