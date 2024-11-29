"""Tests for the utils functions."""

from datetime import date

import pytest

from models import Observation
from utils import get_quarter, is_same_quarter


def test_get_quarter_q1_valid_date():
    """Tests that get_quarter returns 1 for a valid date in Q1."""

    d = date(2024, 1, 1)

    assert get_quarter(d) == 1


def test_get_quarter_q2_valid_date():
    """Tests that get_quarter returns 2 for a valid date in Q2."""

    d = date(2024, 5, 1)

    assert get_quarter(d) == 2


def test_get_quarter_error_invalid_date():
    """Tests that get_quarter raises a TypeError for an invalid date."""

    d = "2024-01-01"

    with pytest.raises(TypeError):
        get_quarter(d)


def test_is_same_quarter_valid_observation_same_quarter():
    """Tests that is_same_quarter returns True for a valid observation in
    the same quarter as the specified date."""

    # Observation in Q1
    observation = Observation(
        date_logged="2024-01-01",
        time_logged="12:00:00",
        time_zone_offset="UTC+0000",
        latitude=0.0,
        longitude=0.0,
        water_temp=0,
        air_temp=0,
        wind_speed=0,
        wind_direction=0,
        humidity=0,
        haze_percent=0,
        precipitation_mm=0,
        radiation_bq=0,
    )

    # Q1 date
    d = date(2024, 1, 1)

    assert is_same_quarter(observation, d)


def test_is_same_quarter_valid_observation_different_quarter():
    """Tests that is_same_quarter returns False for a valid observation in
    a different quarter to the specified date."""

    # Observation in Q1
    observation = Observation(
        date_logged="2024-01-01",
        time_logged="12:00:00",
        time_zone_offset="UTC+0000",
        latitude=0.0,
        longitude=0.0,
        water_temp=0,
        air_temp=0,
        wind_speed=0,
        wind_direction=0,
        humidity=0,
        haze_percent=0,
        precipitation_mm=0,
        radiation_bq=0,
    )

    # Q2 date
    d = date(2024, 4, 1)

    assert not is_same_quarter(observation, d)
