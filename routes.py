"""Defines routes and handler functions."""

from flask import Blueprint

# Create a Flask Blueprint for the routes
api = Blueprint("api", __name__)


@api.route("/hello")
def hello_world():
    """Placeholder endpoint for testing.

    Returns:
        string: Hello World as a string.
    """
    return "Hello World"
