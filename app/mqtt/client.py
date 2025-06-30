import paho.mqtt.client as mqtt
from sqlalchemy.orm import Session
from datetime import datetime
import json
from app.database import SessionLocal
from app.crud import create_air_sample, create_soil_sample
from app.schemas import AirSampleCreate, SoilSampleCreate

# MQTT Configuration
MQTT_BROKER = "localhost"  # Địa chỉ MQTT broker
MQTT_PORT = 1883  # Port mặc định của MQTT
MQTT_USERNAME = "your_username"  # Username MQTT nếu có
MQTT_PASSWORD = "your_password"  # Password MQTT nếu có

# MQTT Topics
TOPIC_AIR = "sensors/air"  # Topic cho sensor không khí
TOPIC_SOIL = "sensors/soil"  # Topic cho sensor độ ẩm đất

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        # Set credentials if needed
        if MQTT_USERNAME and MQTT_PASSWORD:
            self.client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    def connect(self):
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            print(f"Connected to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}")
        except Exception as e:
            print(f"Failed to connect to MQTT Broker: {e}")

    def start(self):
        # Start loop in a non-blocking way
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        # Subscribe to topics
        self.client.subscribe([(TOPIC_AIR, 0), (TOPIC_SOIL, 0)])

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            db = next(get_db())

            if msg.topic == TOPIC_AIR:
                # Expected payload format:
                # {
                #     "temperature": float,
                #     "humidity": float,
                #     "pressure": float
                # }
                sample = AirSampleCreate(
                    temperature=payload["temperature"],
                    humidity=payload["humidity"],
                    pressure=payload["pressure"]
                )
                create_air_sample(db, sample)
                print(f"Saved air sample: {payload}")

            elif msg.topic == TOPIC_SOIL:
                # Expected payload format:
                # {
                #     "description": str,
                #     "soil_moisture": float
                # }
                sample = SoilSampleCreate(
                    description=payload["description"],
                    soil_moisture=payload["soil_moisture"]
                )
                create_soil_sample(db, sample)
                print(f"Saved soil sample: {payload}")

        except Exception as e:
            print(f"Error processing message: {e}")
            if 'db' in locals():
                db.rollback()
        finally:
            if 'db' in locals():
                db.close()

# Sample usage
def start_mqtt_client():
    mqtt_client = MQTTClient()
    mqtt_client.connect()
    mqtt_client.start()
    return mqtt_client
