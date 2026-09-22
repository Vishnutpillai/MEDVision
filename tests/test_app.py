import pytest

from app import create_app
from app.extensions import db
from app.models import User


@pytest.fixture
def app():
    app = create_app()

    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTF_CSRF_ENABLED=False,
    )

    with app.app_context():
        db.create_all()

        user = User(
            name="Test User",
            email="test@example.com",
            role="user",
        )

        user.set_password("TestPassword123")

        db.session.add(user)
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def authenticated_client(app, client):

    response = client.post(
        "/login",
        data={
            "email": "test@example.com",
            "password": "TestPassword123",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    return client


def test_app_exists(app):

    assert app is not None


def test_dashboard(authenticated_client):

    response = authenticated_client.get(
        "/dashboard"
    )

    assert response.status_code == 200


def test_root(client):

    response = client.get("/")

    assert response.status_code == 302
    assert "/login" in response.location


def test_cases_page(authenticated_client):

    response = authenticated_client.get(
        "/cases"
    )

    assert response.status_code == 200


def test_new_case_page(authenticated_client):

    response = authenticated_client.get(
        "/new-case"
    )

    assert response.status_code == 200


def test_analysis_page(authenticated_client):

    response = authenticated_client.get(
        "/analysis"
    )

    assert response.status_code == 200


def test_chat_page(authenticated_client):

    response = authenticated_client.get(
        "/chat"
    )

    assert response.status_code == 200


def test_review_page(authenticated_client):

    response = authenticated_client.get(
        "/review"
    )

    assert response.status_code == 200


def test_analytics_page(authenticated_client):

    response = authenticated_client.get(
        "/analytics"
    )

    assert response.status_code == 200


def test_settings_page(authenticated_client):

    response = authenticated_client.get(
        "/settings"
    )

    assert response.status_code == 200


def test_404_page(client):

    response = client.get(
        "/this-page-does-not-exist"
    )

    assert response.status_code == 404


def test_secret_key_loaded(app):

    assert app.config["SECRET_KEY"]


def test_upload_limit(app):

    assert (
        app.config["MAX_CONTENT_LENGTH"]
        == 10 * 1024 * 1024
    )


def test_dashboard_content(authenticated_client):

    response = authenticated_client.get(
        "/dashboard"
    )

    assert response.status_code == 200
    assert b"Dashboard" in response.data


def test_protected_route_requires_login(client):

    response = client.get(
        "/dashboard"
    )

    assert response.status_code == 302
    assert "/login" in response.location


def test_login_page(client):

    response = client.get(
        "/login"
    )

    assert response.status_code == 200


def test_register_page(client):

    response = client.get(
        "/register"
    )

    assert response.status_code == 200


def test_logout(authenticated_client):

    response = authenticated_client.get(
        "/logout"
    )

    assert response.status_code == 302

    response = authenticated_client.get(
        "/dashboard"
    )

    assert response.status_code == 302