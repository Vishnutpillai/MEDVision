import os

from dotenv import load_dotenv
from flask import Flask, render_template

from app.config import (
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig,
)


load_dotenv()


def create_app():

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    environment = os.getenv(
        "FLASK_ENV",
        "development"
    ).lower()


    # =========================================
    # CONFIGURATION
    # =========================================

    if environment == "production":

        app.config.from_object(
            ProductionConfig
        )

    elif environment == "testing":

        app.config.from_object(
            TestingConfig
        )

    else:

        app.config.from_object(
            DevelopmentConfig
        )


    # =========================================
    # DASHBOARD
    # =========================================

    @app.route("/")
    @app.route("/dashboard")
    def dashboard():

        return render_template(
            "dashboard.html"
        )


    # =========================================
    # CASES
    # =========================================

    @app.route("/cases")
    def cases():

        return render_template(
            "cases.html"
        )


    # =========================================
    # NEW CASE
    # =========================================

    @app.route("/new-case")
    def new_case():

        return render_template(
            "new_case.html"
        )


    # =========================================
    # ANALYSIS
    # =========================================

    @app.route("/analysis")
    def analysis():

        return render_template(
            "analysis.html"
        )


    # =========================================
    # AI CHAT
    # =========================================

    @app.route("/chat")
    def chat():

        return render_template(
            "chat.html"
        )


    # =========================================
    # REVIEW
    # =========================================

    @app.route("/review")
    def review():

        return render_template(
            "review.html"
        )


    # =========================================
    # ANALYTICS
    # =========================================

    @app.route("/analytics")
    def analytics():

        return render_template(
            "analytics.html"
        )


    # =========================================
    # SETTINGS
    # =========================================

    @app.route("/settings")
    def settings():

        return render_template(
            "settings.html"
        )


    # =========================================
    # ERROR HANDLERS
    # =========================================

    @app.errorhandler(404)
    def page_not_found(error):

        return render_template(
            "404.html"
        ), 404


    @app.errorhandler(500)
    def internal_server_error(error):

        return render_template(
            "500.html"
        ), 500

    return app