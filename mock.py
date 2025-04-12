import datetime
import random


def mock_devices():
    for i in range(200):
        yield {
            "id": i,
            "name": f"Device {i}",
            "location": f"Room {random.randint(1, 10)}",
        }


devices = mock_devices()


def get_device_data():
    return {
        "timestamp": datetime.datetime.now().timestamp()
        - random.randint(0, 3600),  # random timestamp within the last hour
        "device_id": random.randint(1, 200),
        "temperature": random.uniform(20.0, 30.0),
        "humidity": random.uniform(40.0, 60.0),
        "pressure": random.uniform(980.0, 1020.0),
        "battery_level": random.randint(20, 100),
        "status": ["online", "offline"][random.randint(0, 1)],
    }


def get_samples():
    # for _ in range(10):
    #     yield get_device_data()
    return [get_device_data() for _ in range(10)]
