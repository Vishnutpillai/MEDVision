from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class User(UserMixin, db.Model):
    """
    Application user model.
    """

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(120),
        nullable=False
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(50),
        nullable=False,
        default="user"
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def set_password(self, password):
        """
        Hash and store the user's password.
        """

        self.password_hash = generate_password_hash(
            password
        )

    def check_password(self, password):
        """
        Verify a password against the stored hash.
        """

        return check_password_hash(
            self.password_hash,
            password
        )

    def __repr__(self):
        return f"<User {self.email}>"