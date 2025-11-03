from sqlalchemy import Column, Integer, String, Date, func
from config.database import Base

class Kategori(Base):
    __tablename__ = "kategori"

    id_kategori = Column(Integer, primary_key=True, index=True, autoincrement=True)
    kategori = Column(String, nullable=False)
    created_at = Column(Date, server_default=func.current_date(), nullable=False)
    updated_at = Column(Date, server_default=func.current_date(), server_onupdate=func.current_date(), nullable=False)
