from sqlalchemy import Column, Integer, String, DateTime, func
from config.database import Base


class Kategori(Base):
    __tablename__ = "kategori"

    id_kategori = Column(Integer, primary_key=True, index=True, autoincrement=True)
    kategori = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), server_onupdate=func.now(), nullable=False)