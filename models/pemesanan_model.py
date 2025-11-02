from sqlalchemy import Column, Integer, String, DateTime
from config.database import Base
from datetime import datetime

class Pemesanan(Base):
    __tablename__ = "pemesanan"

    id_pemesanan = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_pengguna = Column(Integer, nullable=False)
    id_menu = Column(Integer, nullable=False)
    id_kategori = Column(Integer, nullable=False)
    jumlah = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)