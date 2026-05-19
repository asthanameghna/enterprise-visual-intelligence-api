import json
from pathlib import Path

from app.schemas import VisualAnalysisReport

REPORTS_DIR = Path(__file__).resolve().parents[2] / "reports"


def save_report(report: VisualAnalysisReport) -> str:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"{report.report_id}.json"
    report_path.write_text(json.dumps(report.model_dump(), indent=2))
    return report.report_id


def load_report(report_id: str) -> dict:
    report_path = REPORTS_DIR / f"{report_id}.json"
    return json.loads(report_path.read_text())
