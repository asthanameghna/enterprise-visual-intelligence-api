from sqlalchemy import JSON, Column, DateTime, Float, String
from sqlalchemy.sql import func

from app.database import Base


class AnalysisReport(Base):
    __tablename__ = "analysis_reports"

    report_id = Column(String, primary_key=True, index=True)
    input_type = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    detected_entities = Column(JSON, nullable=False)
    visual_facts = Column(JSON, nullable=False)
    issues = Column(JSON, nullable=False)
    retrieved_context = Column(JSON, nullable=False)
    recommended_actions = Column(JSON, nullable=False)
    escalation_level = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    limitations = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())