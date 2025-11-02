from sqlalchemy import Column, Integer, String, DateTime, func
from config.database import Base


class Pemesanan(Base):
    __tablename__ = "pemesanan"

    id_pemesanan = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_pengguna = Column(Integer, nullable=False)
    id_menu = Column(Integer, nullable=False)
    id_kategori = Column(Integer, nullable=False)
    jumlah = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), server_onupdate=func.now(), nullable=False)