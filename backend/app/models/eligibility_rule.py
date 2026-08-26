from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime

from app.database import Base


class EligibilityRule(Base):
    __tablename__ = "eligibility_rules"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)

    scheme_name = Column(String(255), nullable=False)

    max_income = Column(Float, nullable=True)
    min_age = Column(Integer, nullable=True)
    max_age = Column(Integer, nullable=True)

    allowed_categories = Column(String(255), nullable=True)
    allowed_states = Column(String(255), nullable=True)
    student_required = Column(String(10), nullable=True)

    required_documents = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)