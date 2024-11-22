"""Marshmallow schemas for serialising and deserialising JSON data."""

from flask_marshmallow import Marshmallow

import app

ma = Marshmallow(app)


class ObservationSchema(ma.SQLAlchemyAutoSchema):
    """Definition used by serialization library based on User Model"""

    class Meta:
        """Metadata for the ObservationSchema."""

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
        )


obervation_schema = ObservationSchema()
obervations_schema = ObservationSchema(many=True)
