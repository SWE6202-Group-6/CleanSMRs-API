"""Application-related configuration."""

from dotenv import dotenv_values


class Config:
    """Configuration class to expose application configuration values."""

    def __init__(self):
        env_vars = dotenv_values(".env")

        self.secret_key = env_vars["SECRET_KEY"]
        self.website_user = env_vars["WEBSITE_USER"]
        self.website_password = env_vars["WEBSITE_PASSWORD"]
        self.database_uri = env_vars["SQLALCHEMY_DATABASE_URI"]
        self.database_echo = env_vars["SQLALCHEMY_ECHO"]
        self.database_track_modifications = env_vars[
            "SQLALCHEMY_TRACK_MODIFICATIONS"
        ]


config = Config()
