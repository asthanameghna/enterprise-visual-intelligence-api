import json

from openai import OpenAI

from app.config import settings
from app.schemas import VisualFacts


client = OpenAI(api_key=settings.openai_api_key)


def analyze_image_with_vlm(encoded_image: str)-> VisualFacts:
    response = client.responses.create(
        model=settings.openai_model,
        input=[
            {
                "role": "system",
                "content": (
                    "You are an enterprise visual operations analyst. "
                    "Analyze the uploaded image and return ONLY valid JSON. "
                    "detected_entities must be a JSON array of strings. "
                    "visual_facts must be a JSON array of strings. "
                    "possible_risks must be a JSON array of strings. "
                    "Requirements: "
                    "- Always populate detected_entities with concrete visible objects. "
                    "- detected_entities must contain at least 3 items whenever possible. "
                    "- visual_facts should describe observable operational details. "
                    "- possible_risks should identify realistic operational or safety concerns. "
                    "- Keep summaries concise and operationally useful. "
                    "Return JSON with these keys only: input_type, summary, detected_entities, visual_facts, possible_risks. "
                    "Allowed input_type values: retail_shelf, warehouse_scene, equipment_inspection, dashboard_screenshot, inventory_delivery, unknown."
                ),
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{encoded_image}",
                    }
                ],
            },
        ],
        text={"format": {"type": "json_object"}},
    )
    parsed_json = json.loads(response.output_text)

    return VisualFacts(**parsed_json)
