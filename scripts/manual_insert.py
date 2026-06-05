from app.database import SessionLocal
from app.models.analysis_report import AnalysisReport


db = SessionLocal()

report = AnalysisReport(
    report_id="test-001",
    input_type="warehouse_scene",
    summary="Test warehouse report",
    detected_entities=["forklift", "pallet"],
    visual_facts=["forklift operating in aisle"],
    issues=[],
    retrieved_context=[],
    recommended_actions=[],
    escalation_level="low",
    confidence=0.95,
    limitations=[],
)

db.add(report)
db.commit()

print("Report inserted.")