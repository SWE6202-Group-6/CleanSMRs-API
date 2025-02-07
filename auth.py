"""Authentication-related functionality."""

from functools import wraps

import jwt
from flask import jsonify, request

from config import config


def token_required(f):
    """Decorator to require a valid JWT for a route."""

    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            token = token.replace("Bearer ", "")

        if not token:
            return jsonify(message="Token is missing"), 401

        try:
            jwt.decode(token, config.secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify(message="Token has expired"), 401
        except jwt.InvalidTokenError:
            return jsonify(message="Token is invalid"), 401

        return f(*args, **kwargs)

    return decorator
