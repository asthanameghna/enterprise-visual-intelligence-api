import pytest
from pydantic import ValidationError

from app.schemas import Issue, VisualAnalysisReport


def test_visual_analysis_report_valid():
    report = VisualAnalysisReport(
        report_id="report-123",
        input_type="warehouse_scene",
        summary="Warehouse aisle inspection completed.",
        detected_entities=["pallet", "forklift"],
        visual_facts=["A pallet is blocking part of the aisle."],
        issues=[
            Issue(
                issue_type="safety",
                description="Blocked aisle",
                evidence="Pallet positioned in walkway",
                severity="medium",
            )
        ],
        retrieved_context=["Warehouse aisles should remain clear."],
        recommended_actions=["Move pallet to a marked storage area."],
        escalation_level="low",
        confidence=0.92,
        limitations=["Image does not show the full aisle."],
    )

    assert report.input_type == "warehouse_scene"


def test_visual_analysis_report_invalid_input_type():
    with pytest.raises(ValidationError):
        VisualAnalysisReport(
            report_id="report-123",
            input_type="invalid_scene",
            summary="Warehouse aisle inspection completed.",
            detected_entities=["pallet", "forklift"],
            visual_facts=["A pallet is blocking part of the aisle."],
            issues=[],
            retrieved_context=["Warehouse aisles should remain clear."],
            recommended_actions=["Move pallet to a marked storage area."],
            escalation_level="low",
            confidence=0.92,
            limitations=["Image does not show the full aisle."],
        )
