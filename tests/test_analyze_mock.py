from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.schemas import VisualFacts


client = TestClient(app)


def test_analyze_mock():
    mock_visual_facts = VisualFacts(
        input_type="warehouse_scene",
        summary="Warehouse aisle inspection completed.",
        detected_entities=["pallet", "forklift", "walkway"],
        visual_facts=["A pallet is blocking part of the aisle."],
        possible_risks=["Blocked walkway may create a safety risk."],
    )

    with patch(
        "app.routes.analyze.analyze_image_with_vlm",
        return_value=mock_visual_facts,
    ):
        response = client.post(
            "/analyze",
            files={"file": ("test.png", b"image-bytes", "image/png")},
        )

    assert response.status_code == 200
    assert response.json()["input_type"] == "warehouse_scene"
    assert response.json()["summary"] == "Warehouse aisle inspection completed."