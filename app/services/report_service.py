from app.schemas import Issue, VisualAnalysisReport


def generate_mock_report() -> VisualAnalysisReport:
    return VisualAnalysisReport(
        report_id="mock-warehouse-001",
        input_type="warehouse_scene",
        summary="Warehouse aisle shows a pallet partially blocking a marked walkway.",
        detected_entities=["pallet", "forklift lane", "walkway", "storage racks"],
        visual_facts=[
            "A pallet is positioned near the center of the aisle.",
            "The marked pedestrian walkway is partially obstructed.",
        ],
        issues=[
            Issue(
                issue_type="safety_obstruction",
                description="A pallet is blocking part of the pedestrian walkway.",
                evidence="The pallet overlaps the floor markings for the walkway.",
                severity="medium",
            )
        ],
        retrieved_context=[
            "Warehouse walkways should remain clear for safe pedestrian movement.",
            "Temporary obstructions should be moved to designated staging areas.",
        ],
        recommended_actions=[
            "Move the pallet out of the walkway.",
            "Inspect the aisle for additional obstructions.",
        ],
        escalation_level="medium",
        confidence=0.86,
        limitations=["Mock response only. No image was analyzed."],
    )
