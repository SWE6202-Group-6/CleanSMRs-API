"""Script to seed initial data for testing purposes."""

import datetime
import os
import random
import sys

from flask import Flask

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models import Device, Observation, db

app = Flask(__name__)
# If using MySQL, just replace the following lines with the appropriate
# connection string details
db_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "..", "instance", "api.db"
)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def seed_data(num_devices=5, num_observations=20):
    """Seed the database with some initial data for testing purposes. Note that
    this doesn't really reflect real-world data - it's just to get some data in
    to the database so that you can test the API without having to manually add
    records."""

    with app.app_context():
        db.create_all()

        # Create devices
        devices = []
        for i in range(num_devices):
            device = Device(
                name=f"Device {i+1}",
                city=f"City {i+1}",
                country=f"Country {i+1}",
                status="Online",
                battery_level=random.randint(0, 100),
            )
            db.session.add(device)
            devices.append(device)
        db.session.commit()

        # Create observations
        for _ in range(num_observations):
            device = random.choice(devices)
            observation = Observation(
                date_logged=datetime.date(
                    2024, random.randint(1, 12), random.randint(1, 28)
                ),
                time_logged=datetime.time(
                    random.randint(0, 23),
                    random.randint(0, 59),
                    random.randint(0, 59),
                ),
                time_zone_offset=f"+{random.randint(0, 12):02d}:00",
                latitude=random.uniform(-90, 90),
                longitude=random.uniform(-180, 180),
                water_temp=random.randint(-10, 40),
                air_temp=random.randint(-30, 50),
                wind_speed=random.randint(0, 150),
                wind_direction=random.randint(0, 360),
                humidity=random.randint(0, 100),
                haze_percent=random.randint(0, 100),
                precipitation_mm=random.randint(0, 500),
                radiation_bq=random.randint(0, 100),
                device_id=device.id,
            )
            db.session.add(observation)
        db.session.commit()


if __name__ == "__main__":
    seed_data(num_devices=20, num_observations=200)
    print("Data seeded successfully.")
