from datetime import datetime, timezone

from app.extensions import db


class Case(db.Model):

    __tablename__ = "cases"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    case_reference = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    patient_reference = db.Column(
        db.String(100),
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="active"
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False
    )
    
    user = db.relationship(
        "User",
        backref=db.backref(
            "cases",
            lazy=True
        )
    )

    xray_images = db.relationship(
        "XRayImage",
        back_populates="case",
        cascade="all, delete-orphan",
        lazy=True
    )

    medical_reports = db.relationship(
        "MedicalReport",
        back_populates="case",
        cascade="all, delete-orphan",
        lazy=True
    )

    ai_analyses = db.relationship(
        "AIAnalysis",
        back_populates="case",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Case {self.case_reference}>"