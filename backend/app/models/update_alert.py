from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime

from app.database import Base


class UpdateAlert(Base):
    __tablename__ = "update_alerts"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)

    old_hash = Column(String(128), nullable=False)
    new_hash = Column(String(128), nullable=False)
    source_url = Column(Text, nullable=False)

    status = Column(String(20), default="pending")
    detected_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)

    downloaded_file_path = Column(Text, nullable=True)