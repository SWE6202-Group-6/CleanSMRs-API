"""Marshmallow schemas for serialising and deserialising JSON data."""

from flask_marshmallow import Marshmallow

import app
from models import Device, Observation

ma = Marshmallow(app)


class ObservationSchema(ma.SQLAlchemyAutoSchema):
    """Definition used by serialization library based on Observation Model"""

    class Meta:
        """Metadata for the ObservationSchema."""

        model = Observation
        load_instance = True
        ordered = True

        fields = (
            "id",
            "date_logged",
            "time_logged",
            "time_zone_offset",
            "latitude",
            "longitude",
            "water_temp",
            "air_temp",
            "wind_speed",
            "wind_direction",
            "humidity",
            "haze_percent",
            "precipitation_mm",
            "radiation_bq",
            "device_id",
        )


class DeviceSchema(ma.SQLAlchemyAutoSchema):
    """Schema definition for serialising Device entities."""

    class Meta:
        """Metadata for the DeviceSchema."""

        model = Device
        load_instance = True
        ordered = True

        fields = ("id", "name", "city", "country", "status", "battery_level")


obervation_schema = ObservationSchema()
obervations_schema = ObservationSchema(many=True)
