import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from app.schemas import VisualAnalysisReport
from app.services import storage_service


def _minimal_report() -> VisualAnalysisReport:
    return VisualAnalysisReport(
        report_id="test-report-1",
        input_type="unknown",
        summary="Test summary.",
        detected_entities=[],
        visual_facts=[],
        issues=[],
        retrieved_context=[],
        recommended_actions=[],
        escalation_level="none",
        confidence=0.5,
        limitations=[],
    )


def test_save_report_creates_json_file():
    with TemporaryDirectory() as tmp_dir:
        reports_dir = Path(tmp_dir)
        with patch.object(storage_service, "REPORTS_DIR", reports_dir):
            report = _minimal_report()
            storage_service.save_report(report)

            report_path = reports_dir / f"{report.report_id}.json"
            assert report_path.is_file()
            assert json.loads(report_path.read_text()) == report.model_dump()


def test_load_report_returns_saved_content():
    with TemporaryDirectory() as tmp_dir:
        reports_dir = Path(tmp_dir)
        with patch.object(storage_service, "REPORTS_DIR", reports_dir):
            report = _minimal_report()
            storage_service.save_report(report)

            loaded = storage_service.load_report(report.report_id)
            assert loaded == report.model_dump()
