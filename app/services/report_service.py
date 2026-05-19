import uuid

from app.schemas import Issue, VisualAnalysisReport, VisualFacts
from app.services.context_service import get_context_for_input_type


def generate_report_from_visual_facts(
    visual_facts: VisualFacts,
) -> VisualAnalysisReport:
    retrieved_context = get_context_for_input_type(visual_facts.input_type)
    context_text = " ".join(retrieved_context).lower()
    risks_text = " ".join(visual_facts.possible_risks).lower()
    has_risks = bool(visual_facts.possible_risks)
    critical_terms = ("blocked", "exit", "walkway", "fire", "obstruction")

    if (
        has_risks
        and "critical" in context_text
        and any(term in risks_text for term in critical_terms)
    ):
        escalation_level = "critical"
        issue_severity = "critical"
    elif has_risks and "high" in context_text:
        escalation_level = "high"
        issue_severity = "high"
    else:
        escalation_level = "medium" if has_risks else "low"
        issue_severity = "medium"

    issues = [
        Issue(
            issue_type="possible_risk",
            description=risk,
            evidence=risk,
            severity=issue_severity,
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
        retrieved_context=retrieved_context,
        recommended_actions=[
            f"Review and address: {risk}" for risk in visual_facts.possible_risks
        ],
        escalation_level=escalation_level,
        confidence=0.85,
        limitations=["AI-generated analysis; verify findings before acting."],
    )


