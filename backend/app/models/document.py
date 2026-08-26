from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    scheme_name = Column(String(255), nullable=True)
    department = Column(String(255), nullable=True)
    source_url = Column(Text, nullable=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    file_hash = Column(String(128), nullable=True)
    version = Column(String(50), nullable=True)
    academic_year = Column(String(50), nullable=True)
    status = Column(String(50), default="active")
    uploaded_at = Column(DateTime, default=datetime.utcnow)