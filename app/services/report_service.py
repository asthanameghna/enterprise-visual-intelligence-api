import uuid

from app.schemas import Issue, VisualAnalysisReport, VisualFacts


def generate_report_from_visual_facts(
    visual_facts: VisualFacts,
) -> VisualAnalysisReport:
    issues = [
        Issue(
            issue_type="possible_risk",
            description=risk,
            evidence=risk,
            severity="medium",
        )
        for risk in visual_facts.possible_risks
    ]

    return VisualAnalysisReport(
        report_id=str(uuid.uuid4()),
        input_type=visual_facts.input_type,
        summary=visual_facts.summary,
        detected_entities=visual_facts.detected_entities,
        visual_facts=visual_facts.visual_facts,
        issues=issues,
        retrieved_context=[
            "Placeholder context for future retrieval-augmented analysis."
        ],
        recommended_actions=[
            f"Review and address: {risk}" for risk in visual_facts.possible_risks
        ],
        escalation_level="medium" if visual_facts.possible_risks else "low",
        confidence=0.85,
        limitations=["AI-generated analysis; verify findings before acting."],
    )


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
