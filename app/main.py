from fastapi import FastAPI
from app.routers import air, soil
from app.mqtt.client import start_mqtt_client

app = FastAPI()

# Khởi động MQTT client
mqtt_client = start_mqtt_client()

@app.on_event("shutdown")
async def shutdown_event():
    # Dừng MQTT client khi tắt ứng dụng
    mqtt_client.stop()

app.include_router(air.router)
app.include_router(soil.router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
