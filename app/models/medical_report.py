from datetime import datetime, timezone

from app.extensions import db


class MedicalReport(db.Model):
    __tablename__ = "medical_reports"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    case_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "cases.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    file_name = db.Column(
        db.String(255),
        nullable=False
    )

    file_path = db.Column(
        db.String(500),
        nullable=True
    )

    extracted_text = db.Column(
        db.Text,
        nullable=True
    )

    processing_status = db.Column(
        db.String(30),
        nullable=False,
        default="pending"
    )

    chunk_count = db.Column(
        db.Integer,
        nullable=True
    )

    uploaded_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    case = db.relationship(
        "Case",
        back_populates="medical_reports"
    )

    def __repr__(self):
        return f"<MedicalReport {self.file_name}>"