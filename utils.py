"""Utility functions."""

from datetime import date, datetime, timezone

from models import Observation


def is_same_quarter(observation, base_date=datetime.now(timezone.utc)):
    """Checks whether an observation is in the same quarter as a given date."""

    if not isinstance(observation, Observation):
        raise TypeError("observation must be an Observation")

    if not isinstance(base_date, date):
        raise TypeError("base_date must be a date")

    obs_date = observation.date_logged
    obs_time = observation.time_logged

    # Remove UTC from the offset.
    offset = observation.time_zone_offset.replace("UTC", "")

    # Create a datetime and convert the observation date/time to UTC.
    dt = datetime.strptime(
        f"{obs_date} {obs_time}{offset}", "%Y-%m-%d %H:%M:%S%z"
    ).astimezone(timezone.utc)

    return get_quarter(dt.date()) == get_quarter(base_date)


def get_quarter(date_to_check):
    """Returns the quarter of the year for a given date."""

    if not isinstance(date_to_check, date):
        raise TypeError("Expected a date object")

    match date_to_check.month:
        case 1 | 2 | 3:
            return 1
        case 4 | 5 | 6:
            return 2
        case 7 | 8 | 9:
            return 3
        case 10 | 11 | 12:
            return 4
