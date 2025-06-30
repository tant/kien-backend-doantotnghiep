# schemas.py
from datetime import datetime
from pydantic import BaseModel

class AirSampleBase(BaseModel):
    temperature: float
    humidity: float
    pressure: float

class AirSampleCreate(AirSampleBase):
    pass

class AirSampleCreateWithTimestamp(AirSampleBase):
    timestamp: datetime

class AirSample(AirSampleBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True

class SoilSampleBase(BaseModel):
    description: str
    soil_moisture: float

class SoilSampleCreate(SoilSampleBase):
    pass

class SoilSampleCreateWithTimestamp(SoilSampleBase):
    timestamp: datetime

class SoilSample(SoilSampleBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True
