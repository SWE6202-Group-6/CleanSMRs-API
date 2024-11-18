"""CleanSMRs Web API"""

from flask import Flask

app = Flask(__name__)


@app.get("/")
def hello_world():
    """Placeholder endpoint for testing.

    Returns:
        string: Hello World as a string.
    """
    return "Hello World"
