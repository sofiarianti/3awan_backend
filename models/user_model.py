from sqlalchemy import Column, Integer, String, DateTime, func
from config.database import Base


class Pengguna(Base):
    __tablename__ = "pengguna"

    id_pengguna = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), server_onupdate=func.now(), nullable=False)
    role = Column(String, nullable=False)