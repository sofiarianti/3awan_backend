from sqlalchemy import Column, Integer, String, DateTime
from config.database import Base
from datetime import datetime

class Pengguna(Base):
    __tablename__ = "pengguna"

    id_pengguna = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)