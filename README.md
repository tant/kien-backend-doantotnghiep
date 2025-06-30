# FastAPI SQLite Backend

A simple FastAPI backend using SQLite as the database for IoT sensors.

## Cấu trúc thư mục
- `app/`: Chứa mã nguồn chính
  - `models.py`: Định nghĩa các model database
  - `schemas.py`: Định nghĩa các schema Pydantic
  - `crud.py`: Các hàm thao tác với database
  - `database.py`: Cấu hình database
  - `routers/`: API routes
  - `mqtt/`: Module kết nối MQTT
- `tests/`: Chứa các test

## Cài đặt
```bash
# Tạo và kích hoạt môi trường ảo
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# hoặc
.venv\Scripts\activate  # Windows

# Cài đặt các thư viện
pip install -r requirements.txt
```

## Chạy ứng dụng
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Dữ liệu không khí (Air Data)

1. Tạo mẫu dữ liệu không khí (tự động lấy thời gian hiện tại)
```bash
POST /air/samples/

# Ví dụ với curl:
curl -X POST "http://localhost:8000/air/samples/" \
-H "Content-Type: application/json" \
-d '{
    "temperature": 26.5,
    "humidity": 70.2,
    "pressure": 1012.8
}'
```

2. Tạo mẫu dữ liệu không khí với timestamp tùy chọn
```bash
POST /air/samples/with-timestamp/

# Ví dụ với curl:
curl -X POST "http://localhost:8000/air/samples/with-timestamp/" \
-H "Content-Type: application/json" \
-d '{
    "temperature": 25.6,
    "humidity": 65.4,
    "pressure": 1013.2,
    "timestamp": "2025-06-30T15:30:00.000Z"
}'
```

3. Lấy danh sách dữ liệu không khí
```bash
GET /air/samples/
# Tham số:
# - skip: số bản ghi bỏ qua (mặc định: 0)
# - limit: số bản ghi tối đa trả về (mặc định: 100)

# Ví dụ với curl:
curl "http://localhost:8000/air/samples/?skip=0&limit=50"
```

4. Lấy dữ liệu không khí trong 1 tuần gần nhất
```bash
GET /air/samples/weekly/

# Ví dụ với curl:
curl "http://localhost:8000/air/samples/weekly/"
```

### Dữ liệu độ ẩm đất (Soil Data)

1. Tạo mẫu dữ liệu độ ẩm đất (tự động lấy thời gian hiện tại)
```bash
POST /soil/samples/

# Ví dụ với curl:
curl -X POST "http://localhost:8000/soil/samples/" \
-H "Content-Type: application/json" \
-d '{
    "description": "Cây cam số 1",
    "soil_moisture": 42.5
}'
```

2. Tạo mẫu dữ liệu độ ẩm đất với timestamp tùy chọn
```bash
POST /soil/samples/with-timestamp/

# Ví dụ với curl:
curl -X POST "http://localhost:8000/soil/samples/with-timestamp/" \
-H "Content-Type: application/json" \
-d '{
    "description": "Cây cam số 1",
    "soil_moisture": 42.5,
    "timestamp": "2025-06-30T15:30:00.000Z"
}'
```

3. Lấy danh sách dữ liệu độ ẩm đất
```bash
GET /soil/samples/
# Tham số:
# - skip: số bản ghi bỏ qua (mặc định: 0)
# - limit: số bản ghi tối đa trả về (mặc định: 100)

# Ví dụ với curl:
curl "http://localhost:8000/soil/samples/?skip=0&limit=50"
```

4. Lấy dữ liệu độ ẩm đất của một vị trí trong 1 tuần gần nhất
```bash
GET /soil/samples/weekly/{description}

# Ví dụ với curl:
curl "http://localhost:8000/soil/samples/weekly/Cây%20cam%20số%201"
```

## MQTT Integration

Server tự động kết nối với MQTT broker và lắng nghe các topic:
- `sensors/air`: Nhận dữ liệu không khí
- `sensors/soil`: Nhận dữ liệu độ ẩm đất

Format message MQTT:
```json
// Topic: sensors/air
{
    "temperature": float,
    "humidity": float,
    "pressure": float
}

// Topic: sensors/soil
{
    "description": string,
    "soil_moisture": float
}
```

## Lưu ý
- Timestamp sử dụng định dạng ISO 8601
- Các giá trị đo đều là số thực (float)
- API docs có sẵn tại: http://localhost:8000/docs
