from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentResponse(BaseModel):
    id: int
    title: str
    scheme_name: Optional[str] = None
    department: Optional[str] = None
    source_url: Optional[str] = None
    file_name: str
    file_hash: Optional[str] = None
    version: Optional[str] = None
    academic_year: Optional[str] = None
    status: str
    uploaded_at: datetime

    class Config:
        from_attributes = True