from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import SessionLocal
from typing import List

router = APIRouter(prefix="/soil", tags=["soil"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/samples/", response_model=schemas.SoilSample)
def create_soil_sample(sample: schemas.SoilSampleCreate, db: Session = Depends(get_db)):
    return crud.create_soil_sample(db, sample)

@router.get("/samples/", response_model=List[schemas.SoilSample])
def read_soil_samples(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_soil_samples(db, skip=skip, limit=limit)

@router.get("/samples/weekly/{description}", response_model=List[schemas.SoilSample])
def read_soil_samples_weekly_by_description(
    description: str,
    db: Session = Depends(get_db)
):
    """
    Lấy dữ liệu độ ẩm đất của một vị trí/cây cụ thể trong 1 tuần gần nhất.
    Dữ liệu được sắp xếp theo thời gian từ cũ đến mới.
    """
    return crud.get_soil_samples_by_description_last_week(db, description)

@router.post("/samples/with-timestamp/", response_model=schemas.SoilSample)
def create_soil_sample_with_time(
    sample: schemas.SoilSampleCreateWithTimestamp,
    db: Session = Depends(get_db)
):
    """
    Tạo mẫu dữ liệu độ ẩm đất với timestamp được chỉ định.
    Body request cần có dạng:
    {
        "description": string,
        "soil_moisture": float,
        "timestamp": "2025-06-30T10:00:00.000Z"
    }
    """
    return crud.create_soil_sample_with_timestamp(db, sample)
