"""CleanSMRs Web API"""

from dotenv import dotenv_values
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from models import db
from routes import api as api_blueprint
from schemas import ma

# Load the configuration from the .env file
config = dotenv_values(".env")

app = Flask(__name__)

# Configure the app from the loaded configuration
app.config["SQLALCHEMY_DATABASE_URI"] = config["SQLALCHEMY_DATABASE_URI"]
app.config["SQLALCHEMY_ECHO"] = config["SQLALCHEMY_ECHO"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
]

# Initialise the database and Marshmallow
db.init_app(app)
ma.init_app(app)

# Register the API blueprint for our route handlers
app.register_blueprint(api_blueprint, url_prefix="/api")

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/openapi.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "CleanSMRs"
    }) 
app.register_blueprint(swaggerui_blueprint)