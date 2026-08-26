from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.update_alert import UpdateAlert
from app.services.pdf_service import extract_text_from_pdf
from app.services.text_service import split_text_into_chunks
from app.services.chroma_service import store_document_chunks
from datetime import datetime


def approve_update(db: Session, alert_id: int) -> dict:
    alert = db.query(UpdateAlert).filter(UpdateAlert.id == alert_id).first()

    if not alert:
        raise ValueError("Alert not found")

    if alert.status != "pending":
        raise ValueError(f"Alert already {alert.status}")

    old_document = db.query(Document).filter(Document.id == alert.document_id).first()
    if not old_document:
        raise ValueError("Original document not found")

    old_document.status = "archived"

    new_document = Document(
        title=old_document.title,
        scheme_name=old_document.scheme_name,
        department=old_document.department,
        source_url=old_document.source_url,
        file_name=old_document.file_name,
        file_path=alert.downloaded_file_path,
        file_hash=alert.new_hash,
        version=_increment_version(old_document.version),
        academic_year=old_document.academic_year,
        status="active"
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    extracted_text = extract_text_from_pdf(alert.downloaded_file_path)
    chunks = split_text_into_chunks(extracted_text)

    store_document_chunks(
        document_id=new_document.id,
        chunks=chunks,
        metadata={
            "title": new_document.title,
            "scheme_name": new_document.scheme_name or "",
            "department": new_document.department or "",
            "source_url": new_document.source_url or "",
            "academic_year": new_document.academic_year or "",
            "version": new_document.version or "",
            "file_name": new_document.file_name
        }
    )

    alert.status = "approved"
    alert.reviewed_at = datetime.utcnow()
    db.commit()

    return {
        "message": "Update approved and applied",
        "old_document_id": old_document.id,
        "new_document_id": new_document.id,
        "chunk_count": len(chunks)
    }


def reject_update(db: Session, alert_id: int) -> dict:
    alert = db.query(UpdateAlert).filter(UpdateAlert.id == alert_id).first()

    if not alert:
        raise ValueError("Alert not found")

    if alert.status != "pending":
        raise ValueError(f"Alert already {alert.status}")

    alert.status = "rejected"
    alert.reviewed_at = datetime.utcnow()
    db.commit()

    return {"message": "Update rejected"}


def _increment_version(current_version):
    if not current_version:
        return "v2"
    try:
        num = int(current_version.lower().replace("v", ""))
        return f"v{num + 1}"
    except ValueError:
        return f"{current_version}-updated"