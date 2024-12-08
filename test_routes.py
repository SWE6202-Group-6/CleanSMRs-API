"""Tests for the API routes."""

import base64
from datetime import date, time

import pytest
from flask import Flask

from app import api_blueprint as api
from models import Observation
from schemas import ObservationSchema


@pytest.fixture
def client():
    """Fixture to set up a test client for the API."""

    app = Flask(__name__)
    app.register_blueprint(api)
    app.config["TESTING"] = True

    with app.app_context():
        yield app.test_client()


def test_login_valid_credentials(client, monkeypatch):
    """Tests the login route with valid credentials."""

    # Set the configuration values for authentication
    monkeypatch.setattr("config.config.website_user", "user")
    monkeypatch.setattr("config.config.website_password", "password")
    monkeypatch.setattr("config.config.secret_key", "test_secret")

    # Base64 encode the username and password
    encoded_creds = base64.b64encode(b"user:password").decode("utf-8")

    # Make a login request
    response = client.get(
        "/login", headers={"Authorization": f"Basic {encoded_creds}"}
    )

    assert response.status_code == 200
    assert "token" in response.json


def test_login_invalid_credentials(client, monkeypatch):
    """Tests the login route with invalid credentials."""

    # Set the configuration values for authentication
    monkeypatch.setattr("config.config.website_user", "user")
    monkeypatch.setattr("config.config.website_password", "password")
    monkeypatch.setattr("config.config.secret_key", "test_secret")

    # Base64 encode the username and password
    encoded_creds = base64.b64encode(b"user:invalid").decode("utf-8")

    # Make a login request
    response = client.get(
        "/login", headers={"Authorization": f"Basic {encoded_creds}"}
    )

    assert response.status_code == 401
    assert "message" in response.json
    assert response.json["message"] == "Invalid credentials"


def test_get_observations_no_token(client):
    """Tests the get observations route without a token."""

    response = client.get("/observations")

    assert response.status_code == 401
    assert "message" in response.json
    assert response.json["message"] == "Token is missing"


def test_get_observations_valid_token(client, mocker):
    """Tests the GET endpoint returns observations with a valid token."""

    observation = Observation(
        id=1,
        date_logged=date(2024, 1, 1),
        time_logged=time(12, 0, 0),
        time_zone_offset="UTC+00:00",
        latitude=10.0,
        longitude=20.0,
        water_temp=10,
        air_temp=20,
        wind_speed=7,
        wind_direction=180,
        humidity=10,
        haze_percent=10,
        precipitation_mm=0,
        radiation_bq=5,
    )

    mock_query = mocker.patch("models.Observation.query")
    mock_query.all.return_value = [observation]

    # Mock jwt.decode returning a value - any value will do
    mocker.patch("jwt.decode", return_value={"valid": "token"})

    # Make a request with a valid token
    response = client.get(
        "/observations", headers={"Authorization": "Bearer valid_token"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    expected_data = ObservationSchema().dump(observation)
    assert data[0] == expected_data
