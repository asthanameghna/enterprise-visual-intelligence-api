from typing import Literal

from pydantic import BaseModel


class Issue(BaseModel):
    issue_type: str
    description: str
    evidence: str
    severity: Literal["low", "medium", "high", "critical"]


class VisualFacts(BaseModel):
    input_type: Literal[
        "retail_shelf",
        "warehouse_scene",
        "equipment_inspection",
        "dashboard_screenshot",
        "inventory_delivery",
        "unknown",
    ]
    summary: str
    detected_entities: list[str]
    visual_facts: list[str]
    possible_risks: list[str]

