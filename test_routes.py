"""Tests for the API routes."""

import base64

import pytest
from flask import Flask

from app import api_blueprint as api


@pytest.fixture
def client():
    """Fixture to set up a test client for the API."""

    app = Flask(__name__)
    app.register_blueprint(api)
    app.config["TESTING"] = True
    yield app.test_client()


def test_login_success(client):
    """Tests the login route with valid credentials."""

    # Base64 encode the username and password
    encoded_creds = base64.b64encode(b"demo:demo").decode("utf-8")

    # Make a login request
    response = client.get(
        "/login", headers={"Authorization": f"Basic {encoded_creds}"}
    )

    assert response.status_code == 200
    assert "token" in response.json


def test_login_failure(client):
    """Tests the login route with invalid credentials."""

    # Base64 encode the username and password
    encoded_creds = base64.b64encode(b"demo:wrong").decode("utf-8")

    # Make a login request
    response = client.get(
        "/login", headers={"Authorization": f"Basic {encoded_creds}"}
    )

    assert response.status_code == 401
    assert "message" in response.json
    assert response.json["message"] == "Invalid credentials"
