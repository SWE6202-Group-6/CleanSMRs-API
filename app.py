"""CleanSMRs Web API"""

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from config import config
from models import db
from routes import api as api_blueprint
from schemas import ma

app = Flask(__name__)

# Configure the app from the loaded configuration
app.config["SQLALCHEMY_DATABASE_URI"] = config.database_uri
app.config["SQLALCHEMY_ECHO"] = config.database_echo
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
    config.database_track_modifications
)

# Ensure that JSON responses are ordered according to our specified field order
app.json.sort_keys = False

# Initialise the database and Marshmallow
db.init_app(app)
ma.init_app(app)

# Register the API blueprint for our route handlers
app.register_blueprint(api_blueprint)

SWAGGER_URL = "/api/docs"  # URL for exposing Swagger UI (without trailing '/')
API_URL = "/static/openapi.json"

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={"app_name": "CleanSMRs"},  # Swagger UI config overrides
)
app.register_blueprint(swaggerui_blueprint)
