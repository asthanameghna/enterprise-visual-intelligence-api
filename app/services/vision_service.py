from openai import OpenAI

from app.config import settings


client = OpenAI(api_key=settings.openai_api_key)


def analyze_image_with_vlm(encoded_image: str):
    return {"summary": "placeholder"}
