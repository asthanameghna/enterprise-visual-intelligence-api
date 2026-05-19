from fastapi import APIRouter, File, UploadFile

from app.schemas import VisualAnalysisReport
from app.services.report_service import generate_report_from_visual_facts
from app.services.storage_service import save_report
from app.services.vision_service import analyze_image_with_vlm
from app.utils.image_utils import encode_image_to_base64, validate_image_file

router = APIRouter()


@router.post("/analyze", response_model=VisualAnalysisReport)
def analyze(file: UploadFile = File(...)):
    validate_image_file(file)
    image_bytes = file.file.read()
    encoded_image = encode_image_to_base64(image_bytes)
    visual_facts = analyze_image_with_vlm(encoded_image)

    report = generate_report_from_visual_facts(visual_facts)
    save_report(report)
    return report
