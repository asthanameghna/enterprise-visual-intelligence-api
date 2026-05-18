from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_analyze_mock():
    mock_report = {
        "report_id": "mock-123",
        "input_type": "warehouse_scene",
        "summary": "Warehouse aisle inspection completed.",
    }

    with patch(
        "app.routes.analyze.report_service.generate_mock_report",
        return_value=mock_report,
    ):
        response = client.post(
            "/analyze",
            files={"file": ("test.png", b"image-bytes", "image/png")},
        )

    assert response.status_code == 200
    assert response.json()["report_id"] == "mock-123"
    assert response.json()["input_type"] == "warehouse_scene"
