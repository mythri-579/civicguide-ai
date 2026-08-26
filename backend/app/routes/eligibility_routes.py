from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.eligibility_rule import EligibilityRule
from app.schemas.eligibility import (
    EligibilityRuleCreate,
    EligibilityCheckRequest,
    EligibilityCheckResponse
)
from app.services.eligibility_service import check_eligibility

router = APIRouter(prefix="/api/eligibility", tags=["Eligibility"])


@router.post("/rules")
def create_rule(rule_data: EligibilityRuleCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(EligibilityRule)
        .filter(EligibilityRule.scheme_name.ilike(rule_data.scheme_name))
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Rules for scheme '{rule_data.scheme_name}' already exist. Use update instead."
        )

    rule = EligibilityRule(**rule_data.model_dump())
    db.add(rule)
    db.commit()
    db.refresh(rule)

    return {"message": "Eligibility rule created", "rule_id": rule.id}


@router.get("/rules")
def list_rules(db: Session = Depends(get_db)):
    return db.query(EligibilityRule).all()


@router.post("/check", response_model=EligibilityCheckResponse)
def check(request: EligibilityCheckRequest, db: Session = Depends(get_db)):
    result = check_eligibility(
        db=db,
        scheme_name=request.scheme_name,
        age=request.age,
        income=request.income,
        category=request.category,
        is_student=request.is_student,
        state=request.state
    )
    return result