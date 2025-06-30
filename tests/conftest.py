import pytest
from fastapi.testclient import TestClient
from app.database import Base, engine
from app.main import app

@pytest.fixture(autouse=True)
def setup_database():
    # Tạo tất cả bảng trước mỗi test
    Base.metadata.create_all(bind=engine)
    yield
    # Xóa tất cả bảng sau mỗi test
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)
