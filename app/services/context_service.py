from pathlib import Path


CONTEXT_DOCS_DIR = Path(__file__).resolve().parents[2] / "context_docs"

CONTEXT_BY_INPUT_TYPE = {
    "warehouse_scene": CONTEXT_DOCS_DIR / "warehouse_safety_rules.md",
    "retail_shelf": CONTEXT_DOCS_DIR / "retail_shelf_rules.md",
    "inventory_delivery": CONTEXT_DOCS_DIR / "inventory_escalation_policy.md",
    "equipment_inspection": CONTEXT_DOCS_DIR / "equipment_inspection_rules.md",
    "dashboard_screenshot": CONTEXT_DOCS_DIR / "dashboard_anomaly_policy.md",
}


def get_context_for_input_type(input_type: str) -> list[str]:
    context_path = CONTEXT_BY_INPUT_TYPE.get(input_type)
    if context_path is None or not context_path.exists():
        return []

    return [context_path.read_text()]
