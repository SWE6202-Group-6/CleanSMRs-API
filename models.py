"""Database models for the API."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Observation(db.Model):
    """Definition of the Observation Model used by SQLAlchemy"""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_logged = db.Column(db.Date, nullable=False)
    time_logged = db.Column(db.Time, nullable=False)
    time_zone_offset = db.Column(db.String(80), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    water_temp = db.Column(db.Integer, nullable=False)
    air_temp = db.Column(db.Integer, nullable=False)
    wind_speed = db.Column(db.Integer, nullable=False)
    wind_direction = db.Column(db.Integer, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    haze_percent = db.Column(db.Integer, nullable=False)
    precipitation_mm = db.Column(db.Integer, nullable=False)
    radiation_bq = db.Column(db.Integer, nullable=False)
    device = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)


class Device(db.Model):
    """Definition of the Device Model for an IoT device."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(15), nullable=False)
    battery_level = db.Column(db.Integer, nullable=False)
