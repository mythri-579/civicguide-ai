from sqlalchemy.orm import Session

from app.models.eligibility_rule import EligibilityRule


def check_eligibility(
    db: Session,
    scheme_name: str,
    age: int,
    income: float,
    category: str,
    is_student: bool,
    state: str
) -> dict:

    rule = (
        db.query(EligibilityRule)
        .filter(EligibilityRule.scheme_name.ilike(scheme_name))
        .first()
    )

    if not rule:
        return {
            "eligible": False,
            "reason": f"No eligibility rules found for scheme '{scheme_name}'. Please contact admin to add rules for this scheme.",
            "required_documents": []
        }

    reasons_failed = []

    if rule.max_income is not None and income > rule.max_income:
        reasons_failed.append(
            f"Your income (Rs. {income:,.0f}) exceeds the allowed limit of Rs. {rule.max_income:,.0f}."
        )

    if rule.min_age is not None and age < rule.min_age:
        reasons_failed.append(f"You must be at least {rule.min_age} years old.")

    if rule.max_age is not None and age > rule.max_age:
        reasons_failed.append(f"You must be at most {rule.max_age} years old.")

    if rule.allowed_categories:
        allowed_list = [c.strip().lower() for c in rule.allowed_categories.split(",")]
        if category.strip().lower() not in allowed_list:
            reasons_failed.append(
                f"Your category '{category}' is not in the allowed list ({rule.allowed_categories})."
            )

    if rule.allowed_states and rule.allowed_states.strip().upper() != "ALL":
        allowed_states_list = [s.strip().lower() for s in rule.allowed_states.split(",")]
        if state.strip().lower() not in allowed_states_list:
            reasons_failed.append(
                f"This scheme is not available in your state '{state}'."
            )

    if rule.student_required and rule.student_required.lower() == "yes" and not is_student:
        reasons_failed.append("This scheme requires you to be a current student.")

    required_docs = []
    if rule.required_documents:
        required_docs = [doc.strip() for doc in rule.required_documents.split(",")]

    if reasons_failed:
        return {
            "eligible": False,
            "reason": " ".join(reasons_failed),
            "required_documents": required_docs
        }

    return {
        "eligible": True,
        "reason": "You meet all the eligibility criteria for this scheme.",
        "required_documents": required_docs
    }