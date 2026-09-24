import os

from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# BASE CONFIGURATION
# ============================================================

class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key-change-me"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = (
        int(os.getenv("MAX_UPLOAD_SIZE_MB", "16"))
        * 1024
        * 1024
    )

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = False


# ============================================================
# DEVELOPMENT CONFIGURATION
# ============================================================

class DevelopmentConfig(Config):

    DEBUG = True


# ============================================================
# PRODUCTION CONFIGURATION
# ============================================================

class ProductionConfig(Config):

    DEBUG = False

    SESSION_COOKIE_SECURE = True


# ============================================================
# TESTING CONFIGURATION
# ============================================================

class TestingConfig(Config):

    TESTING = True

    WTF_CSRF_ENABLED = False