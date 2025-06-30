# crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, timedelta

# --- Air Sample CRUD ---

def create_air_sample(db: Session, sample: schemas.AirSampleCreate):
    """
    Tạo một mẫu dữ liệu không khí mới với timestamp được tự động gán là thời điểm hiện tại.

    Args:
        db (Session): The database session.
        sample (schemas.AirSampleCreate): Dữ liệu mẫu không khí đầu vào (không bao gồm timestamp).

    Returns:
        models.AirSample: Đối tượng mẫu không khí đã được tạo và lưu vào database.
    """
    db_sample = models.AirSample(**sample.dict())
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    return db_sample

def create_air_sample_with_timestamp(db: Session, sample: schemas.AirSampleCreateWithTimestamp):
    """
    Tạo mẫu dữ liệu không khí với timestamp được chỉ định.
    Hữu ích cho việc tạo dữ liệu test hoặc nhập dữ liệu lịch sử.

    Args:
        db (Session): The database session.
        sample (schemas.AirSampleCreateWithTimestamp): Dữ liệu mẫu không khí
            bao gồm cả timestamp.

    Returns:
        models.AirSample: Đối tượng mẫu không khí đã được tạo.
    """
    db_sample = models.AirSample(**sample.dict())
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    return db_sample

def get_air_samples(db: Session, skip: int = 0, limit: int = 100):
    """
    Lấy danh sách các mẫu dữ liệu không khí, hỗ trợ phân trang.
    Sắp xếp theo thời gian giảm dần (mới nhất trước).

    Args:
        db (Session): The database session.
        skip (int): Số lượng bản ghi bỏ qua.
        limit (int): Số lượng bản ghi tối đa trả về.

    Returns:
        list[models.AirSample]: Danh sách các mẫu dữ liệu không khí.
    """
    return db.query(models.AirSample).order_by(models.AirSample.timestamp.desc()).offset(skip).limit(limit).all()

def get_air_samples_last_week(db: Session):
    """
    Lấy tất cả các mẫu dữ liệu không khí trong vòng 7 ngày gần nhất.
    Sắp xếp theo thời gian tăng dần (cũ nhất trước), phù hợp cho việc vẽ đồ thị.

    Args:
        db (Session): The database session.

    Returns:
        list[models.AirSample]: Danh sách các mẫu dữ liệu không khí trong tuần qua.
    """
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    return db.query(models.AirSample)\
        .filter(models.AirSample.timestamp >= one_week_ago)\
        .order_by(models.AirSample.timestamp.asc())\
        .all()

# --- Soil Sample CRUD ---

def create_soil_sample(db: Session, sample: schemas.SoilSampleCreate):
    """
    Tạo một mẫu dữ liệu độ ẩm đất mới với timestamp được tự động gán.

    Args:
        db (Session): The database session.
        sample (schemas.SoilSampleCreate): Dữ liệu mẫu độ ẩm đất đầu vào.

    Returns:
        models.SoilSample: Đối tượng mẫu độ ẩm đất đã được tạo.
    """
    db_sample = models.SoilSample(**sample.dict())
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    return db_sample

def create_soil_sample_with_timestamp(db: Session, sample: schemas.SoilSampleCreateWithTimestamp):
    """
    Tạo mẫu dữ liệu độ ẩm đất với timestamp được chỉ định.
    Hữu ích cho việc tạo dữ liệu test hoặc nhập dữ liệu lịch sử.

    Args:
        db (Session): The database session.
        sample (schemas.SoilSampleCreateWithTimestamp): Dữ liệu mẫu độ ẩm đất
            bao gồm cả timestamp.

    Returns:
        models.SoilSample: Đối tượng mẫu độ ẩm đất đã được tạo.
    """
    db_sample = models.SoilSample(**sample.dict())
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    return db_sample

def get_soil_samples(db: Session, skip: int = 0, limit: int = 100):
    """
    Lấy danh sách các mẫu dữ liệu độ ẩm đất, hỗ trợ phân trang.
    Sắp xếp theo thời gian giảm dần (mới nhất trước).

    Args:
        db (Session): The database session.
        skip (int): Số lượng bản ghi bỏ qua.
        limit (int): Số lượng bản ghi tối đa trả về.

    Returns:
        list[models.SoilSample]: Danh sách các mẫu dữ liệu độ ẩm đất.
    """
    return db.query(models.SoilSample).order_by(models.SoilSample.timestamp.desc()).offset(skip).limit(limit).all()

def get_soil_samples_by_description_last_week(db: Session, description: str):
    """
    Lấy tất cả các mẫu dữ liệu độ ẩm đất của một vị trí cụ thể
    trong vòng 7 ngày gần nhất. Sắp xếp theo thời gian tăng dần.

    Args:
        db (Session): The database session.
        description (str): Mô tả vị trí/cây cần lọc.

    Returns:
        list[models.SoilSample]: Danh sách các mẫu dữ liệu độ ẩm đất.
    """
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    return db.query(models.SoilSample)\
        .filter(models.SoilSample.description == description)\
        .filter(models.SoilSample.timestamp >= one_week_ago)\
        .order_by(models.SoilSample.timestamp.asc())\
        .all()
