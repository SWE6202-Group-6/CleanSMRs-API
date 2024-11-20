"""CleanSMRs Web API"""

from dotenv import dotenv_values
from flask import Flask

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


@app.get("/")
def hello_world():
    """Placeholder endpoint for testing.

    Returns:
        string: Hello World as a string.
    """
    return "Hello World"
