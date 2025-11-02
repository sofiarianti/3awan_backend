from sqlalchemy import Column, Integer, String, DateTime
from config.database import Base
from datetime import datetime

class Pembayaran(Base):
    __tablename__ = "pembayaran"

    id_pembayaran = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_pemesanan = Column(Integer, nullable=False)
    id_pengguna = Column(Integer, nullable=False)
    id_menu = Column(Integer, nullable=False)
    id_kategori = Column(Integer, nullable=False)
    metode_pembayaran = Column(String, nullable=False)
    qr_code_url = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)