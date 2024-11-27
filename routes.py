"""Defines routes and handler functions."""

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from models import db
from schemas import ObservationSchema

# Create a Flask Blueprint for the routes
api = Blueprint("api", __name__)


@api.route("/observations/create", methods=["POST"])
def create_observation():
    """Creates a new Observation record."""

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
