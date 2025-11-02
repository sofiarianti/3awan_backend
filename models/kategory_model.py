from sqlalchemy import Column, Integer, String, DateTime
from config.database import Base
from datetime import datetime

class Kategori(Base):
    __tablename__ = "kategori"

    id_kategori = Column(Integer, primary_key=True, index=True, autoincrement=True)
    kategori = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)