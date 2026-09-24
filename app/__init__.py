import os
import secrets

from datetime import datetime, timezone

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
    login_required,
    login_user,
    logout_user,
)

from werkzeug.utils import secure_filename

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

from app.models import (
    User,
    Case,
    XRayImage,
    MedicalReport,
    AIAnalysis,
)


# ============================================================
# ALLOWED FILE EXTENSIONS
# ============================================================

ALLOWED_XRAY_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
}

ALLOWED_REPORT_EXTENSIONS = {
    "pdf",
}


# ============================================================
# CASE REFERENCE GENERATOR
# ============================================================

def generate_case_reference():
    """
    Generate a unique human-readable case reference.

    Example:
        CASE-20260923-A1B2C3
    """

    date_part = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d")

    random_part = secrets.token_hex(
        3
    ).upper()

    return f"CASE-{date_part}-{random_part}"


# ============================================================
# FILE VALIDATION
# ============================================================

def allowed_file(filename, allowed_extensions):
    """
    Check whether a filename has an allowed extension.
    """

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in allowed_extensions


# ============================================================
# STORED FILE NAME GENERATOR
# ============================================================

def generate_upload_filename(original_filename):
    """
    Generate a safe unique filename.
    """

    safe_name = secure_filename(
        original_filename
    )

    random_part = secrets.token_hex(
        8
    )

    return f"{random_part}_{safe_name}"


# ============================================================
# APPLICATION FACTORY
# ============================================================

def create_app():

    # --------------------------------------------------------
    # CREATE FLASK APPLICATION
    # --------------------------------------------------------

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    # ========================================================
    # CONFIGURATION
    # ========================================================

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

    # ========================================================
    # UPLOAD FOLDER
    # ========================================================

    app.config.setdefault(
        "UPLOAD_FOLDER",
        os.path.join(
            app.instance_path,
            "uploads"
        )
    )

    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )

    # ========================================================
    # FLASK EXTENSIONS
    # ========================================================

    db.init_app(app)

    migrate.init_app(
        app,
        db,
    )

    login_manager.init_app(
        app
    )

    csrf.init_app(
        app
    )

    # ========================================================
    # FLASK-LOGIN USER LOADER
    # ========================================================

    @login_manager.user_loader
    def load_user(user_id):

        try:

            return db.session.get(
                User,
                int(user_id),
            )

        except (
            TypeError,
            ValueError,
        ):

            return None

    # ========================================================
    # REGISTER
    # ========================================================

    @app.route(
        "/register",
        methods=["GET", "POST"],
    )
    def register():

        if current_user.is_authenticated:

            return redirect(
                url_for("dashboard")
            )

        # ----------------------------------------------------
        # SHOW REGISTRATION PAGE
        # ----------------------------------------------------

        if request.method == "GET":

            return render_template(
                "auth/register.html"
            )

        # ----------------------------------------------------
        # READ FORM DATA
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # VALIDATE NAME
        # ----------------------------------------------------

        if not name:

            flash(
                "Name is required.",
                "danger",
            )

            return redirect(
                url_for("register")
            )

        # ----------------------------------------------------
        # VALIDATE EMAIL
        # ----------------------------------------------------

        if not email:

            flash(
                "Email is required.",
                "danger",
            )

            return redirect(
                url_for("register")
            )

        # ----------------------------------------------------
        # VALIDATE PASSWORD LENGTH
        # ----------------------------------------------------

        if len(password) < 8:

            flash(
                "Password must contain at least 8 characters.",
                "danger",
            )

            return redirect(
                url_for("register")
            )

        # ----------------------------------------------------
        # VALIDATE PASSWORD COMPLEXITY
        # ----------------------------------------------------

        if password.isalpha() or password.isdigit():

            flash(
                "Password must contain letters and numbers.",
                "danger",
            )

            return redirect(
                url_for("register")
            )

        # ----------------------------------------------------
        # CONFIRM PASSWORD
        # ----------------------------------------------------

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger",
            )

            return redirect(
                url_for("register")
            )

        # ----------------------------------------------------
        # CHECK EXISTING USER
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # CREATE USER
        # ----------------------------------------------------

        user = User(
            name=name,
            email=email,
            role="user",
        )

        user.set_password(
            password
        )

        # ----------------------------------------------------
        # SAVE USER
        # ----------------------------------------------------

        try:

            db.session.add(
                user
            )

            db.session.commit()

        except Exception as error:

            db.session.rollback()

            print(
                "REGISTRATION ERROR:",
                repr(error)
            )

            flash(
                "Unable to create the account. Please try again.",
                "danger",
            )

            return redirect(
                url_for("register")
            )

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        flash(
            "Account created successfully. Please log in.",
            "success",
        )

        return redirect(
            url_for("login")
        )

    # ========================================================
    # LOGIN
    # ========================================================

    @app.route(
        "/login",
        methods=["GET", "POST"],
    )
    def login():

        if current_user.is_authenticated:

            return redirect(
                url_for("dashboard")
            )

        # ----------------------------------------------------
        # SHOW LOGIN PAGE
        # ----------------------------------------------------

        if request.method == "GET":

            return render_template(
                "auth/login.html"
            )

        # ----------------------------------------------------
        # READ FORM DATA
        # ----------------------------------------------------

        email = request.form.get(
            "email",
            "",
        ).strip().lower()

        password = request.form.get(
            "password",
            "",
        )

        # ----------------------------------------------------
        # VALIDATE FORM
        # ----------------------------------------------------

        if not email or not password:

            flash(
                "Email and password are required.",
                "danger",
            )

            return redirect(
                url_for("login")
            )

        # ----------------------------------------------------
        # FIND USER
        # ----------------------------------------------------

        user = db.session.scalar(
            db.select(User).where(
                User.email == email
            )
        )

        # ----------------------------------------------------
        # VERIFY PASSWORD
        # ----------------------------------------------------

        if (
            user is None
            or not user.check_password(password)
        ):

            flash(
                "Invalid email or password.",
                "danger",
            )

            return redirect(
                url_for("login")
            )

        # ----------------------------------------------------
        # LOGIN
        # ----------------------------------------------------

        login_user(
            user
        )

        flash(
            "Login successful.",
            "success",
        )

        return redirect(
            url_for("dashboard")
        )

    # ========================================================
    # LOGOUT
    # ========================================================

    @app.route(
        "/logout"
    )
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

    # ========================================================
    # ROOT ROUTE
    # ========================================================

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        return redirect(url_for("login"))
    # ========================================================
    # DASHBOARD
    # ========================================================

    @app.route("/dashboard")
    @login_required
    def dashboard():

        cases = db.session.scalars(
            db.select(Case)
            .where(
                Case.user_id == current_user.id
            )
            .order_by(
                Case.created_at.desc()
            )
        ).all()

        total_cases = len(cases)

        completed_cases = sum(
            1
            for case in cases
            if case.status == "completed"
        )

        pending_cases = sum(
            1
            for case in cases
            if case.status in [
                "active",
                "pending"
            ]
        )

        review_cases = sum(
            1
            for case in cases
            if case.status in [
                "review",
                "needs_review"
            ]
        )

        return render_template(
            "dashboard.html",
            total_cases=total_cases,
            completed_cases=completed_cases,
            pending_cases=pending_cases,
            review_cases=review_cases,
            recent_cases=cases[:5],
        )

    # ========================================================
    # CASE LIST
    # ========================================================

    @app.route(
        "/cases"
    )
    @login_required
    def cases():

        user_cases = db.session.scalars(
            db.select(Case)
            .where(
                Case.user_id == current_user.id
            )
            .order_by(
                Case.created_at.desc()
            )
        ).all()

        return render_template(
            "cases.html",
            cases=user_cases,
        )

    # ========================================================
    # CASE DETAIL
    # ========================================================

    @app.route(
        "/cases/<int:case_id>"
    )
    @login_required
    def case_detail(case_id):

        case = db.session.scalar(
            db.select(Case).where(
                Case.id == case_id,
                Case.user_id == current_user.id,
            )
        )

        if case is None:

            return render_template(
                "404.html"
            ), 404

        return render_template(
            "case_detail.html",
            case=case,
        )

    # ========================================================
    # CREATE NEW CASE
    # ========================================================

    @app.route(
        "/new-case",
        methods=["GET", "POST"],
    )
    @login_required
    def new_case():

        if request.method == "POST":

            title = request.form.get(
                "title",
                "",
            ).strip()

            patient_reference = request.form.get(
                "patient_reference",
                "",
            ).strip()

            if not title:

                flash(
                    "Case title is required.",
                    "danger",
                )

                return redirect(
                    url_for("new_case")
                )

            if not patient_reference:

                flash(
                    "Patient reference is required.",
                    "danger",
                )

                return redirect(
                    url_for("new_case")
                )

            case = Case(
                user_id=current_user.id,
                case_reference=generate_case_reference(),
                patient_reference=patient_reference,
                title=title,
                status="active",
            )

            try:

                db.session.add(
                    case
                )

                db.session.commit()

            except Exception as error:

                db.session.rollback()

                print(
                    "CASE CREATION ERROR:",
                    repr(error)
                )

                flash(
                    "Unable to create the case. Please try again.",
                    "danger",
                )

                return redirect(
                    url_for("new_case")
                )

            flash(
                "Case created successfully.",
                "success",
            )

            return redirect(
                url_for(
                    "case_detail",
                    case_id=case.id,
                )
            )

        return render_template(
            "new_case.html"
        )

    # ========================================================
    # UPLOAD CHEST X-RAY
    # ========================================================

    @app.route(
        "/cases/<int:case_id>/xray",
        methods=["POST"]
    )
    @login_required
    def upload_xray(case_id):

        case = db.session.scalar(
            db.select(Case).where(
                Case.id == case_id,
                Case.user_id == current_user.id,
            )
        )

        if case is None:

            return render_template(
                "404.html"
            ), 404

        file = request.files.get(
            "xray_file"
        )

        if file is None or file.filename == "":

            flash(
                "Please select an X-ray image.",
                "danger"
            )

            return redirect(
                url_for(
                    "case_detail",
                    case_id=case.id
                )
            )

        if not allowed_file(
            file.filename,
            ALLOWED_XRAY_EXTENSIONS
        ):

            flash(
                "Invalid X-ray format. Please upload PNG, JPG, or JPEG.",
                "danger"
            )

            return redirect(
                url_for(
                    "case_detail",
                    case_id=case.id
                )
            )

        original_filename = secure_filename(
            file.filename
        )

        if not original_filename:

            flash(
                "Invalid X-ray filename.",
                "danger"
            )

            return redirect(
                url_for(
                    "case_detail",
                    case_id=case.id
                )
            )

        stored_filename = generate_upload_filename(
            original_filename
        )

        case_upload_folder = os.path.join(
            app.config["UPLOAD_FOLDER"],
            "xrays",
            str(case.id)
        )

        os.makedirs(
            case_upload_folder,
            exist_ok=True
        )

        file_path = os.path.join(
            case_upload_folder,
            stored_filename
        )

        try:

            file.save(
                file_path
            )

        except Exception as error:

            print(
                "X-RAY FILE SAVE ERROR:",
                repr(error)
            )

            flash(
                "Unable to save X-ray file.",
                "danger"
            )

            return redirect(
                url_for(
                    "case_detail",
                    case_id=case.id
                )
            )

        file_extension = (
            original_filename
            .rsplit(
                ".",
                1
            )[1]
            .lower()
        )

        file_size = os.path.getsize(
            file_path
        )

        xray = XRayImage(
            case_id=case.id,
            file_name=original_filename,
            file_path=file_path,
            image_format=file_extension,
            file_size=file_size,
        )

        try:

            db.session.add(
                xray
            )

            db.session.commit()

        except Exception as error:

            db.session.rollback()

            print(
                "X-RAY DATABASE ERROR:",
                repr(error)
            )

            if os.path.exists(
                file_path
            ):

                os.remove(
                    file_path
                )

            flash(
                "Unable to save X-ray information.",
                "danger"
            )

            return redirect(
                url_for(
                    "case_detail",
                    case_id=case.id
                )
            )

        flash(
            "X-ray uploaded successfully.",
            "success"
        )

        return redirect(
            url_for(
                "case_detail",
                case_id=case.id
            )
        )

    # ========================================================
    # UPLOAD MEDICAL REPORT
    # ========================================================

    @app.route(
        "/cases/<int:case_id>/report",
        methods=["POST"]
    )
    @login_required
    def upload_report(case_id):

        case = db.session.scalar(
            db.select(Case).where(
                Case.id == case_id,
                Case.user_id == current_user.id,
            )
        )

        if case is None:

            return render_template(
                "404.html"
            ), 404

        file = request.files.get(
            "report_file"
        )

        if file is None or file.filename == "":

            flash(
                "Please select a medical report PDF.",
                "danger"
            )

            return redirect(
                url_for(
                    "case_detail",
                    case_id=case.id
                )
            )

        if not allowed_file(
            file.filename,
            ALLOWED_REPORT_EXTENSIONS
        ):

            flash(
                "Invalid report format. Please upload a PDF file.",
                "danger"
            )

            return redirect(
                url_for(
                    "case_detail",
                    case_id=case.id
                )
            )

        original_filename = secure_filename(
            file.filename
        )

        if not original_filename:

            flash(
                "Invalid medical report filename.",
                "danger"
            )

            return redirect(
                url_for(
                    "case_detail",
                    case_id=case.id
                )
            )

        stored_filename = generate_upload_filename(
            original_filename
        )

        report_upload_folder = os.path.join(
            app.config["UPLOAD_FOLDER"],
            "reports",
            str(case.id)
        )

        os.makedirs(
            report_upload_folder,
            exist_ok=True
        )

        file_path = os.path.join(
            report_upload_folder,
            stored_filename
        )

        try:

            file.save(
                file_path
            )

        except Exception as error:

            print(
                "MEDICAL REPORT FILE SAVE ERROR:",
                repr(error)
            )

            flash(
                "Unable to save medical report.",
                "danger"
            )

            return redirect(
                url_for(
                    "case_detail",
                    case_id=case.id
                )
            )

        report = MedicalReport(
            case_id=case.id,
            file_name=original_filename,
            file_path=file_path,
            processing_status="pending",
        )

        try:

            db.session.add(
                report
            )

            db.session.commit()

        except Exception as error:

            db.session.rollback()

            print(
                "MEDICAL REPORT DATABASE ERROR:",
                repr(error)
            )

            if os.path.exists(
                file_path
            ):

                os.remove(
                    file_path
                )

            flash(
                "Unable to save medical report information.",
                "danger"
            )

            return redirect(
                url_for(
                    "case_detail",
                    case_id=case.id
                )
            )

        flash(
            "Medical report uploaded successfully.",
            "success"
        )

        return redirect(
            url_for(
                "case_detail",
                case_id=case.id
            )
        )

    # ========================================================
    # AI ANALYSIS
    # ========================================================

    @app.route(
        "/analysis"
    )
    @login_required
    def analysis():

        return render_template(
            "analysis.html"
        )

    # ========================================================
    # AI CHAT
    # ========================================================

    @app.route(
        "/chat"
    )
    @login_required
    def chat():

        return render_template(
            "chat.html"
        )

    # ========================================================
    # CLINICAL REVIEW
    # ========================================================

    @app.route(
        "/review"
    )
    @login_required
    def review():

        return render_template(
            "review.html"
        )

    # ========================================================
    # ANALYTICS
    # ========================================================

    @app.route(
        "/analytics"
    )
    @login_required
    def analytics():

        return render_template(
            "analytics.html"
        )

    # ========================================================
    # SETTINGS
    # ========================================================

    @app.route(
        "/settings"
    )
    @login_required
    def settings():

        return render_template(
            "settings.html"
        )

    # ========================================================
    # 404 ERROR
    # ========================================================

    @app.errorhandler(404)
    def page_not_found(error):

        return render_template(
            "404.html"
        ), 404

    # ========================================================
    # 500 ERROR
    # ========================================================

    @app.errorhandler(500)
    def internal_server_error(error):

        return render_template(
            "500.html"
        ), 500

    # ========================================================
    # RETURN APPLICATION
    # ========================================================

    return app