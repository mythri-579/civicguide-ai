from pydantic import BaseModel, Field
from typing import Optional


class EligibilityRuleCreate(BaseModel):
    scheme_name: str
    document_id: Optional[int] = None
    max_income: Optional[float] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    allowed_categories: Optional[str] = None
    allowed_states: Optional[str] = None
    student_required: Optional[str] = "any"
    required_documents: Optional[str] = None


class EligibilityCheckRequest(BaseModel):
    scheme_name: str
    age: int = Field(..., ge=0, le=120)
    income: float = Field(..., ge=0)
    category: str
    is_student: bool
    state: str


class EligibilityCheckResponse(BaseModel):
    eligible: bool
    reason: str
    required_documents: list[str] = []