from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL database dari Railway
DATABASE_URL = "postgresql://postgres:HNbcOdTzHuGccXpOLkNQFGBiYoODrSbX@yamanote.proxy.rlwy.net:53455/railway"
# Engine koneksi
engine = create_engine(DATABASE_URL, echo=True)
# Session untuk query
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base untuk model ORM
Base = declarative_base()
# Dependency untuk session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
