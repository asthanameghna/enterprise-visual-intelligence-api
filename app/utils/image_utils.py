from fastapi import HTTPException, UploadFile


ALLOWED_IMAGE_CONTENT_TYPES = {"image/jpeg", "image/jpg", "image/png"}


def validate_image_file(file: UploadFile) -> bool:
    if file.content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image file type")

    return True
