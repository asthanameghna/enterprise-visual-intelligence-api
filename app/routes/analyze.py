from fastapi import APIRouter, File, UploadFile

from app.services import report_service
from app.services.vision_service import analyze_image_with_vlm
from app.utils.image_utils import encode_image_to_base64, validate_image_file

router = APIRouter()


@router.post("/analyze")
def analyze(file: UploadFile = File(...)):
    validate_image_file(file)
    image_bytes = file.file.read()
    encoded_image = encode_image_to_base64(image_bytes)
    vlm_result = analyze_image_with_vlm(encoded_image)

    return report_service.generate_mock_report()
