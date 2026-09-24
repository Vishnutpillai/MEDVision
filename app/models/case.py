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
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    case_reference = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
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
        db.String(30),
        nullable=False,
        default="active"
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # --------------------------------------------------
    # Relationship with User
    # --------------------------------------------------

    user = db.relationship(
        "User",
        back_populates="cases"
    )

    # --------------------------------------------------
    # Relationship with X-Ray images
    # --------------------------------------------------

    xray_images = db.relationship(
        "XRayImage",
        back_populates="case",
        cascade="all, delete-orphan"
    )

    # --------------------------------------------------
    # Relationship with medical reports
    # --------------------------------------------------

    medical_reports = db.relationship(
        "MedicalReport",
        back_populates="case",
        cascade="all, delete-orphan"
    )

    # --------------------------------------------------
    # Relationship with AI analyses
    # --------------------------------------------------

    ai_analyses = db.relationship(
        "AIAnalysis",
        back_populates="case",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Case {self.case_reference}>"