"""Defines routes and handler functions."""

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from models import Observation, db
from schemas import ObservationSchema

# Create a Flask Blueprint for the routes
api = Blueprint("api", __name__)


@api.route("/observations/create", methods=["POST"])
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
