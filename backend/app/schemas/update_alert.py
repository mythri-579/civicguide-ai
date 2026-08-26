from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UpdateAlertResponse(BaseModel):
    id: int
    document_id: int
    old_hash: str
    new_hash: str
    source_url: str
    status: str
    detected_at: datetime
    reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True