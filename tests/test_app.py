import pytest

from app import create_app


@pytest.fixture
def app():

    app = create_app()

    app.config.update(
        TESTING=True
    )

    yield app


@pytest.fixture
def client(app):

    return app.test_client()


# =========================================
# APPLICATION TEST
# =========================================

def test_app_exists(app):

    assert app is not None


# =========================================
# DASHBOARD
# =========================================

def test_dashboard(client):

    response = client.get("/dashboard")

    assert response.status_code == 200


# =========================================
# ROOT
# =========================================

def test_root(client):

    response = client.get("/")

    assert response.status_code == 200


# =========================================
# CASES
# =========================================

def test_cases_page(client):

    response = client.get("/cases")

    assert response.status_code == 200


# =========================================
# NEW CASE
# =========================================

def test_new_case_page(client):

    response = client.get("/new-case")

    assert response.status_code == 200


# =========================================
# ANALYSIS
# =========================================

def test_analysis_page(client):

    response = client.get("/analysis")

    assert response.status_code == 200


# =========================================
# AI CHAT
# =========================================

def test_chat_page(client):

    response = client.get("/chat")

    assert response.status_code == 200


# =========================================
# REVIEW
# =========================================

def test_review_page(client):

    response = client.get("/review")

    assert response.status_code == 200


# =========================================
# ANALYTICS
# =========================================

def test_analytics_page(client):

    response = client.get("/analytics")

    assert response.status_code == 200


# =========================================
# SETTINGS
# =========================================

def test_settings_page(client):

    response = client.get("/settings")

    assert response.status_code == 200


# =========================================
# 404 ERROR
# =========================================

def test_404_page(client):

    response = client.get(
        "/this-route-does-not-exist"
    )

    assert response.status_code == 404

    assert b"Page Not Found" in response.data
# =========================================
# CONFIGURATION
# =========================================

def test_secret_key_loaded(app):

    assert app.config["SECRET_KEY"] is not None


def test_upload_limit(app):

    assert app.config["MAX_CONTENT_LENGTH"] > 0

# =========================================
# DASHBOARD TEMPLATE CONTENT
# =========================================

def test_dashboard_content(client):

    response = client.get("/dashboard")

    assert b"Dashboard" in response.data
    assert b"Total Cases" in response.data
    assert b"Recent Cases" in response.data
    assert b"AI System Status" in response.data