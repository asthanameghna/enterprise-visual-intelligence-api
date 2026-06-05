from app.database import SessionLocal
from app.models.analysis_report import AnalysisReport
from app.schemas import VisualAnalysisReport, Issue


def save_report_to_db(report: VisualAnalysisReport) -> str:
    db = SessionLocal()

    db_report = AnalysisReport(
        report_id=report.report_id,
        input_type=report.input_type,
        summary=report.summary,
        detected_entities=report.detected_entities,
        visual_facts=report.visual_facts,
        issues=[issue.model_dump() for issue in report.issues],
        retrieved_context=report.retrieved_context,
        recommended_actions=report.recommended_actions,
        escalation_level=report.escalation_level,
        confidence=report.confidence,
        limitations=report.limitations,
    )

    db.add(db_report)
    db.commit()
    db.close()

    return report.report_id

def load_report_from_db(report_id: str) -> VisualAnalysisReport | None:
    db = SessionLocal()

    report = (
        db.query(AnalysisReport)
        .filter(AnalysisReport.report_id == report_id)
        .first()
    )

    db.close()

    if report is None:
        return None

    return VisualAnalysisReport(
        report_id=report.report_id,
        input_type=report.input_type,
        summary=report.summary,
        detected_entities=report.detected_entities,
        visual_facts=report.visual_facts,
        issues=[Issue(**issue) for issue in report.issues],
        retrieved_context=report.retrieved_context,
        recommended_actions=report.recommended_actions,
        escalation_level=report.escalation_level,
        confidence=report.confidence,
        limitations=report.limitations,
    )