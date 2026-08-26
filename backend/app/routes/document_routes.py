import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.config import UPLOAD_DIR
from app.database import get_db
from app.models.document import Document
from app.services.chroma_service import store_document_chunks
from app.services.pdf_service import extract_text_from_pdf
from app.services.text_service import split_text_into_chunks
from app.utils.file_utils import calculate_file_hash
from app.utils.auth_dependency import require_admin
from app.models.user import User

router = APIRouter(prefix="/api/documents", tags=["Documents"])

@router.post("/upload")
def upload_document(
    title: str = Form(...),
    scheme_name: str = Form(None),
    department: str = Form(None),
    source_url: str = Form(None),
    version: str = Form(None),
    academic_year: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    upload_path = Path(UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)

    saved_file_path = upload_path / file.filename

    with open(saved_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_hash = calculate_file_hash(str(saved_file_path))
    extracted_text = extract_text_from_pdf(str(saved_file_path))

    document = Document(
        title=title,
        scheme_name=scheme_name,
        department=department,
        source_url=source_url,
        file_name=file.filename,
        file_path=str(saved_file_path),
        file_hash=file_hash,
        version=version,
        academic_year=academic_year,
        status="active"
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    chunks = split_text_into_chunks(extracted_text)

    chunk_count = store_document_chunks(
        document_id=document.id,
        chunks=chunks,
        metadata={
            "title": title,
            "scheme_name": scheme_name or "",
            "department": department or "",
            "source_url": source_url or "",
            "version": version or "",
            "academic_year": academic_year or "",
            "file_name": file.filename
        }
    )

    return {
        "message": "Document uploaded and indexed successfully",
        "document_id": document.id,
        "file_name": document.file_name,
        "file_hash": document.file_hash,
        "chunk_count": chunk_count,
        "extracted_text_preview": extracted_text[:1000]
    }


@router.get("/")
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).order_by(Document.uploaded_at.desc()).all()

    return documents