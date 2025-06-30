from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import SessionLocal
from typing import List

router = APIRouter(prefix="/air", tags=["air"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/samples/", response_model=schemas.AirSample)
def create_air_sample(sample: schemas.AirSampleCreate, db: Session = Depends(get_db)):
    return crud.create_air_sample(db, sample)

@router.get("/samples/", response_model=List[schemas.AirSample])
def read_air_samples(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_air_samples(db, skip=skip, limit=limit)

@router.get("/samples/weekly/", response_model=List[schemas.AirSample])
def read_air_samples_weekly(db: Session = Depends(get_db)):
    """
    Lấy dữ liệu không khí (nhiệt độ, độ ẩm, áp suất) trong 1 tuần gần nhất.
    Dữ liệu được sắp xếp theo thời gian từ cũ đến mới.
    """
    return crud.get_air_samples_last_week(db)

@router.post("/samples/with-timestamp/", response_model=schemas.AirSample)
def create_air_sample_with_time(
    sample: schemas.AirSampleCreateWithTimestamp,
    db: Session = Depends(get_db)
):
    """
    Tạo mẫu dữ liệu không khí với timestamp được chỉ định.
    Body request cần có dạng:
    {
        "temperature": float,
        "humidity": float,
        "pressure": float,
        "timestamp": "2025-06-30T10:00:00.000Z"
    }
    """
    return crud.create_air_sample_with_timestamp(db, sample)
