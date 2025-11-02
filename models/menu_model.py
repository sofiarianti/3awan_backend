from sqlalchemy import Column, Integer, String, DateTime, func
from config.database import Base


class Menu(Base):
    __tablename__ = "menu"

    id_menu = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama_makanan = Column(String, nullable=False)
    id_kategori = Column(Integer, nullable=False)
    harga = Column(Integer, nullable=False)
    deskripsi = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), server_onupdate=func.now(), nullable=False)