"""Defines routes and handler functions."""

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from models import Observation, db
from schemas import ObservationSchema

# Create a Flask Blueprint for the routes
api = Blueprint("api", __name__)


@api.route("/observations", methods=["POST"])
def create_observation():
    """Creates a new Observation record.

    Returns:
        Response: A JSON representation of the created observation.
    """

    # Loading the request JSON into an Observation instance using the schema
    # will carry out basic validation, ensuring all fields are provided or else
    # raising an exception. We could further expand this by ensuring values
    # provided are within valid ranges, e.g. wind speed is between 0 and 360.
    #
    # TODO: Add additional validation to ensure all properties are valid.
    try:
        # Attempt to load the request JSON into an Observation using the schema
        observation = ObservationSchema().load(request.get_json())

        # Add the new observation to the database
        db.session.add(observation)
        db.session.commit()

        return ObservationSchema().jsonify(observation), 201
    except ValidationError as error:
        # Return any validation errors as JSON along with a Bad Request status
        # code.
        return jsonify(error.messages), 400


@api.route("/observations/<int:observation_id>", methods=["PUT"])
def put_observation(observation_id):
    """Perform a full update of an existing Observation record.

    Args:
        observation_id (int): The ID of the observation to update.

    Returns:
        Response: A JSON representation of the updated observation.
    """

    observation = Observation.query.filter_by(id=observation_id).first()
    if not observation:
        return jsonify({"error": "Observation not found"}), 404

    try:
        data = request.get_json()
        if id in data and data["id"] != observation_id:
            return jsonify(error="ID in request body does not match URL"), 400

        # Setting instance=observation updates the entity we've retrieved from
        # the database with the new data provided in the request JSON.
        observation = ObservationSchema().load(data, instance=observation)
        db.session.commit()

        return ObservationSchema().jsonify(observation), 200
    except ValidationError as error:
        return jsonify(error.messages), 400


@api.route("/observations/<int:observation_id>", methods=["PATCH"])
def patch_observation(observation_id):
    """Perform a partial update of an existing Observation record.

    Args:
        observation_id (int): The ID of the observation to update.

    Returns:
        Response: A JSON representation of the updated observation.
    """

    observation = Observation.query.filter_by(id=observation_id).first()
    if not observation:
        return jsonify({"error": "Observation not found"}), 404

    try:
        data = request.get_json()

        if not data:
            return jsonify(error="At least one property is required"), 400

        if id in data and data["id"] != observation_id:
            return jsonify(error="ID in request body does not match URL"), 400

        # Setting partial=True allows us to perform a partial update on the
        # entity, only updating the fields provided in the request JSON.
        observation = ObservationSchema().load(
            data, instance=observation, partial=True
        )
        db.session.commit()

        return ObservationSchema().jsonify(observation), 200
    except ValidationError as error:
        return jsonify(error.messages), 400
# START: New GET (parameterised queries)
@api.route("/observations", methods=["GET"])
def get_observations():
    """Retrieves observations based on filtering criteria.

    Returns:
        Response: A JSON representation of the filtered observations.
    """

    # These are the parameters we would be querying on 
    date_from = request.args.get('date_from')  # Format: YYYY-MM-DD
    date_to = request.args.get('date_to')      # Format: YYYY-MM-DD
    min_latitude = request.args.get('min_latitude', type=float)
    max_latitude = request.args.get('max_latitude', type=float)
    min_longitude = request.args.get('min_longitude', type=float)
    max_longitude = request.args.get('max_longitude', type=float)

    # Extraction of the min or max filters for other numeric fields
    filters = {
        "min_water_temp": request.args.get('min_water_temp', type=int),
        "max_water_temp": request.args.get('max_water_temp', type=int),
        "min_air_temp": request.args.get('min_air_temp', type=int),
        "max_air_temp": request.args.get('max_air_temp', type=int),
        "min_wind_speed": request.args.get('min_wind_speed', type=int),
        "max_wind_speed": request.args.get('max_wind_speed', type=int),
        "min_humidity": request.args.get('min_humidity', type=int),
        "max_humidity": request.args.get('max_humidity', type=int),
        "min_haze_percent": request.args.get('min_haze_percent', type=int),
        "max_haze_percent": request.args.get('max_haze_percent', type=int),
        "min_precipitation_mm": request.args.get('min_precipitation_mm', type=int),
        "max_precipitation_mm": request.args.get('max_precipitation_mm', type=int),
        "min_radiation_bq": request.args.get('min_radiation_bq', type=int),
        "max_radiation_bq": request.args.get('max_radiation_bq', type=int),
    }

    # the biulding of the query
    query = Observation.query

    # This is where we apply date range filtering
    if date_from:
        query = query.filter(Observation.date_logged >= date_from)
    if date_to:
        query = query.filter(Observation.date_logged <= date_to)

    # latitude/longitude range filtering
    if min_latitude is not None:
        query = query.filter(Observation.latitude >= min_latitude)
    if max_latitude is not None:
        query = query.filter(Observation.latitude <= max_latitude)
    if min_longitude is not None:
        query = query.filter(Observation.longitude >= min_longitude)
    if max_longitude is not None:
        query = query.filter(Observation.longitude <= max_longitude)

    # numeric filters dynamically
    for key, value in filters.items():
        if value is not None:
            field_name, op = key.split('_')
            field = getattr(Observation, field_name)
            if op == 'min':
                query = query.filter(field >= value)
            elif op == 'max':
                query = query.filter(field <= value)

    # We execute the query lol
    observations = query.all()

    # Then we turn the results into a json response format
    data = ObservationSchema(many=True).dump(observations)

    return jsonify({"data": data, "total": len(data)})
# END