import os


class Config:
    """
    Base application configuration.
    """

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret-key"
    )

    MAX_CONTENT_LENGTH = (
        int(
            os.getenv(
                "MAX_UPLOAD_SIZE_MB",
                "10"
            )
        )
        * 1024
        * 1024
    )

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY",
        ""
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        ""
    )


class DevelopmentConfig(Config):
    """
    Development configuration.
    """

    DEBUG = True


class ProductionConfig(Config):
    """
    Production configuration.
    """

    DEBUG = False


class TestingConfig(Config):
    """
    Testing configuration.
    """

    TESTING = True
    DEBUG = False