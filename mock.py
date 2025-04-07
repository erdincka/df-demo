import datetime
import logging
import random

logger = logging.getLogger("mock")

def mock_devices():
    for i in range(200):
        yield {
            "id": i,
            "name": f"Device {i}",
            "location": f"Room {random.randint(1, 10)}"
        }

devices = mock_devices()

def get_device_data():
    return {
        "device_id": random.randint(1, 200),
        "timestamp": datetime.datetime.now() - datetime.timedelta(seconds=random.randint(0, 3600)),
        "temperature": random.uniform(20.0, 30.0),
        "humidity": random.uniform(40.0, 60.0),
        "pressure": random.uniform(980.0, 1020.0),
        "battery_level": random.randint(20, 100),
        "status": ["online", "offline"][random.randint(0, 1)],
    }

def get_samples():
    for _ in range(10):
        yield get_device_data()

