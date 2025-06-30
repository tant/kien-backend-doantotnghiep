# crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, timedelta

def create_air_sample(db: Session, sample: schemas.AirSampleCreate):
    db_sample = models.AirSample(**sample.dict())
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    return db_sample

def get_air_samples(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AirSample).order_by(models.AirSample.timestamp.desc()).offset(skip).limit(limit).all()

def get_air_samples_last_week(db: Session):
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    return db.query(models.AirSample)\
        .filter(models.AirSample.timestamp >= one_week_ago)\
        .order_by(models.AirSample.timestamp.asc())\
        .all()


def create_soil_sample(db: Session, sample: schemas.SoilSampleCreate):
    db_sample = models.SoilSample(**sample.dict())
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    return db_sample

def get_soil_samples(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SoilSample).order_by(models.SoilSample.timestamp.desc()).offset(skip).limit(limit).all()

def get_soil_samples_by_description_last_week(db: Session, description: str):
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    return db.query(models.SoilSample)\
        .filter(models.SoilSample.description == description)\
        .filter(models.SoilSample.timestamp >= one_week_ago)\
        .order_by(models.SoilSample.timestamp.asc())\
        .all()
