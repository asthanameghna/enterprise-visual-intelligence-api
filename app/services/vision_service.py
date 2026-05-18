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
                "Return only valid JSON matching this schema: "
                "{"
                "\"input_type\": string, "
                "\"summary\": string, "
                "\"detected_entities\": list of strings, "
                "\"visual_facts\": list of strings, "
                "\"possible_risks\": list of strings"
                "}. "
                "input_type must be one of: retail_shelf, warehouse_scene, "
                "equipment_inspection, dashboard_screenshot, inventory_delivery, unknown."
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
