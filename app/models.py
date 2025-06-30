# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class AirSample(Base):
    __tablename__ = "air_samples"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)

class SoilSample(Base):
    __tablename__ = "soil_samples"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    description = Column(String, index=True)
    soil_moisture = Column(Float)
