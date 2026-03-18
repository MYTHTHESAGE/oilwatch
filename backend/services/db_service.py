import os
import uuid
from datetime import datetime
from sqlalchemy import create_engine, Column, Date, Boolean, Float, String, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import UUID

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/oilwatch")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Detection(Base):
    __tablename__ = "detections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    bbox = Column(JSON, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    spill_detected = Column(Boolean, nullable=False, default=False)
    area_km2 = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)
    mask_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
