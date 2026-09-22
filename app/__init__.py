import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from flask_login import (
    current_user,
    login_manager,
    login_required,
    login_user,
    logout_user,
)

from app.config import (
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig,
)

from app.extensions import (
    db,
    login_manager,
    migrate,
    csrf,
)

from app.models import User


def create_app():

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    # =========================================
    # CONFIGURATION
    # =========================================

    environment = os.getenv(
        "FLASK_ENV",
        "development",
    ).lower()

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
    # EXTENSIONS
    # =========================================

    db.init_app(app)

    migrate.init_app(
        app,
        db,
    )

    login_manager.init_app(app)
    csrf.init_app(app)

    # =========================================
    # FLASK-LOGIN USER LOADER
    # =========================================

    @login_manager.user_loader
    def load_user(user_id):

        try:

            return db.session.get(
                User,
                int(user_id),
            )

        except (TypeError, ValueError):

            return None

    # =========================================
    # REGISTRATION
    # =========================================
    @app.route(
    "/register",
    methods=["GET", "POST"],
)
    def register():

    # -----------------------------------------
    # GET REQUEST
    # -----------------------------------------

        if request.method == "GET":

            return render_template(
            "auth/register.html"
        )

        # -----------------------------------------
        # GET FORM DATA
        # -----------------------------------------

        name = request.form.get(
            "name",
            "",
        ).strip()

        email = request.form.get(
            "email",
            "",
        ).strip().lower()

        password = request.form.get(
            "password",
            "",
        )

        confirm_password = request.form.get(
            "confirm_password",
            "",
        )

        # -----------------------------------------
        # BASIC VALIDATION
        # -----------------------------------------

        if not name:

            flash(
                "Name is required.",
                "danger",
            )

            return redirect(
                url_for("register")
            )

        if not email:

            flash(
                "Email is required.",
                "danger",
            )

            return redirect(
                url_for("register")
            )

        # Password must have at least 8 characters
        if len(password) < 8:

            flash(
                "Password must contain at least 8 characters.",
                "danger",
            )

            return redirect(
                url_for("register")
            )

        # Password cannot contain only letters
        # or only numbers
        if password.isalpha() or password.isdigit():

            flash(
                "Password must contain letters and numbers.",
                "danger",
            )

            return redirect(
                url_for("register")
            )

        # Password confirmation
        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger",
            )

            return redirect(
                url_for("register")
            )

        # -----------------------------------------
        # CHECK EXISTING USER
        # -----------------------------------------

        existing_user = db.session.scalar(
            db.select(User).where(
                User.email == email
            )
        )

        if existing_user:

            flash(
                "An account with this email already exists.",
                "warning",
            )

            return redirect(
                url_for("register")
            )

        # -----------------------------------------
        # CREATE USER
        # -----------------------------------------

        user = User(
            name=name,
            email=email,
            role="user",
        )

        # Hash the password before storing it
        user.set_password(
            password
        )

        # -----------------------------------------
        # SAVE USER TO DATABASE
        # -----------------------------------------

        try:

            db.session.add(user)

            db.session.commit()

        except Exception as e:

            # Roll back failed database transaction
            db.session.rollback()

            # Development debugging
            print(
                "REGISTRATION ERROR:",
                repr(e)
            )

            flash(
                "Unable to create the account. Please try again.",
                "danger",
            )

            return redirect(
                url_for("register")
            )

        # -----------------------------------------
        # SUCCESS
        # -----------------------------------------

        flash(
            "Account created successfully. Please log in.",
            "success",
        )

        return redirect(
            url_for("login")
        )

    # =========================================
    # LOGIN
    # =========================================

    @app.route(
        "/login",
        methods=["GET", "POST"],
    )
    def login():

        # -----------------------------------------
        # ALREADY AUTHENTICATED
        # -----------------------------------------

        if current_user.is_authenticated:

            return redirect(
                url_for("dashboard")
            )

        # -----------------------------------------
        # GET REQUEST
        # -----------------------------------------

        if request.method == "GET":

            return render_template(
                "auth/login.html"
            )

        # -----------------------------------------
        # GET FORM DATA
        # -----------------------------------------

        email = request.form.get(
            "email",
            "",
        ).strip().lower()

        password = request.form.get(
            "password",
            "",
        )

        # -----------------------------------------
        # BASIC VALIDATION
        # -----------------------------------------

        if not email or not password:

            flash(
                "Email and password are required.",
                "danger",
            )

            return redirect(
                url_for("login")
            )

        # -----------------------------------------
        # FIND USER
        # -----------------------------------------

        user = db.session.scalar(
            db.select(User).where(
                User.email == email
            )
        )

        # -----------------------------------------
        # VERIFY USER
        # -----------------------------------------

        if user is None or not user.check_password(
            password
        ):

            flash(
                "Invalid email or password.",
                "danger",
            )

            return redirect(
                url_for("login")
            )

        # -----------------------------------------
        # CREATE LOGIN SESSION
        # -----------------------------------------

        login_user(user)

        flash(
            "Login successful.",
            "success",
        )

        return redirect(
            url_for("dashboard")
        )

    # =========================================
    # LOGOUT
    # =========================================

    @app.route("/logout")
    @login_required
    def logout():

        logout_user()

        flash(
            "You have been logged out.",
            "success",
        )

        return redirect(
            url_for("login")
        )

    # =========================================
    # DASHBOARD
    # =========================================

    @app.route("/")
    @app.route("/dashboard")
    @login_required
    def dashboard():

        return render_template(
            "dashboard.html"
        )

    # =========================================
    # CASES
    # =========================================

    @app.route("/cases")
    @login_required
    def cases():

        return render_template(
            "cases.html"
        )

    # =========================================
    # NEW CASE
    # =========================================

    @app.route("/new-case")
    @login_required
    def new_case():

        return render_template(
            "new_case.html"
        )

    # =========================================
    # ANALYSIS
    # =========================================

    @app.route("/analysis")
    @login_required
    def analysis():

        return render_template(
            "analysis.html"
        )

    # =========================================
    # AI CHAT
    # =========================================

    @app.route("/chat")
    @login_required
    def chat():

        return render_template(
            "chat.html"
        )

    # =========================================
    # REVIEW
    # =========================================

    @app.route("/review")
    @login_required
    def review():

        return render_template(
            "review.html"
        )

    # =========================================
    # ANALYTICS
    # =========================================

    @app.route("/analytics")
    @login_required
    def analytics():

        return render_template(
            "analytics.html"
        )

    # =========================================
    # SETTINGS
    # =========================================

    @app.route("/settings")
    @login_required
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

    # =========================================
    # RETURN APPLICATION
    # =========================================

    return app