"""Tests for the API routes."""

import base64
import datetime

import pytest
from flask import Flask

from app import api_blueprint as api
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


def test_get_observations_success(client, mocker):
    """Tests the get observations route with valid credentials."""

    # Mock the JWT decode function to return a valid token - the value is not
    # relevant for this test.
    mocker.patch("jwt.decode", return_value={"valid": "token"})

    # Mock the database query to return a couple of observations
    mock_observations = [
        {
            "date_logged": datetime.date(2024, 1, 1),
            "time_logged": datetime.time(12, 0, 0),
            "time_zone_offset": "UTC+00:00",
            "latitude": 10.0,
            "longitude": 20.0,
            "water_temp": 10,
            "air_temp": 20,
            "wind_speed": 7,
            "wind_direction": 180,
            "humidity": 10,
            "haze_percent": 10,
            "precipitation_mm": 0,
            "radiation_bq": 5,
            "device_id": 1,
        },
        {
            "date_logged": datetime.date(2024, 1, 2),
            "time_logged": datetime.time(13, 0, 0),
            "time_zone_offset": "UTC+00:00",
            "latitude": 15.0,
            "longitude": 25.0,
            "water_temp": 12,
            "air_temp": 22,
            "wind_speed": 8,
            "wind_direction": 190,
            "humidity": 12,
            "haze_percent": 12,
            "precipitation_mm": 1,
            "radiation_bq": 6,
            "device_id": 2,
        },
    ]

    mock_query = mocker.patch("models.Observation.query")
    mock_query.all.return_value = mock_observations

    response = client.get(
        "/observations",
        headers={"Authorization": "Bearer valid_token"},
    )

    assert response.status_code == 200
    assert len(response.json) == 2


def test_create_observation_success(client, mocker):
    """Tests the create observation route with valid data."""

    # Some valid observation data.
    observation_data = {
        "date_logged": "2024-01-01",
        "time_logged": "12:00:00",
        "time_zone_offset": "UTC+00:00",
        "latitude": 10.0,
        "longitude": 20.0,
        "water_temp": 10,
        "air_temp": 20,
        "wind_speed": 7,
        "wind_direction": 180,
        "humidity": 10,
        "haze_percent": 10,
        "precipitation_mm": 0,
        "radiation_bq": 5,
        "device_id": 1,
    }

    # Mock the JWT decode function to return a valid token - the value is not
    # relevant for this test.
    mocker.patch("jwt.decode", return_value={"valid": "token"})

    # Mock the database session so we don't require a database for this test.
    mock_db_session = mocker.patch("models.db.session")

    response = client.post(
        "/observations",
        json=observation_data,
        headers={"Authorization": "Bearer valid_token"},
    )

    assert response.status_code == 201
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()


def test_create_observation_invalid_data(client, mocker):
    """Tests the create observation route with valid data."""

    # Some invalid observation data.
    observation_data = {
        "date_logged": "2024-01-01",
    }

    # Mock the JWT decode function to return a valid token - the value is not
    # relevant for this test.
    mocker.patch("jwt.decode", return_value={"valid": "token"})

    response = client.post(
        "/observations",
        json=observation_data,
        headers={"Authorization": "Bearer valid_token"},
    )

    assert response.status_code == 400
