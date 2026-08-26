import os
import requests

from sqlalchemy.orm import Session
from datetime import datetime

from app.models.document import Document
from app.models.update_alert import UpdateAlert
from app.utils.file_utils import calculate_file_hash
from app.config import UPLOAD_DIR


def check_all_sources(db: Session):
    documents = (
        db.query(Document)
        .filter(Document.status == "active")
        .filter(Document.source_url.isnot(None))
        .filter(Document.source_url != "")
        .all()
    )

    checked_count = 0
    alerts_created = 0

    for doc in documents:
        checked_count += 1
        try:
            alert_created = check_single_source(db, doc)
            if alert_created:
                alerts_created += 1
        except Exception as e:
            print(f"[UpdateMonitor] Failed to check document {doc.id} ({doc.title}): {e}")

    return {"checked": checked_count, "alerts_created": alerts_created}


def check_single_source(db: Session, document: Document) -> bool:
    existing_pending = (
        db.query(UpdateAlert)
        .filter(UpdateAlert.document_id == document.id)
        .filter(UpdateAlert.status == "pending")
        .first()
    )
    if existing_pending:
        return False

    response = requests.get(document.source_url, timeout=30)
    response.raise_for_status()

    temp_filename = f"check_{document.id}_{int(datetime.utcnow().timestamp())}.pdf"
    temp_path = os.path.join(UPLOAD_DIR, "pending_updates", temp_filename)
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)

    with open(temp_path, "wb") as f:
        f.write(response.content)

    new_hash = calculate_file_hash(temp_path)

    if new_hash == document.file_hash:
        os.remove(temp_path)
        return False

    alert = UpdateAlert(
        document_id=document.id,
        old_hash=document.file_hash,
        new_hash=new_hash,
        source_url=document.source_url,
        status="pending",
        downloaded_file_path=temp_path
    )
    db.add(alert)
    db.commit()

    return True