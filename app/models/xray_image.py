from datetime import datetime, timezone

from app.extensions import db


class XRayImage(db.Model):
    __tablename__ = "xray_images"

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

    image_format = db.Column(
        db.String(20),
        nullable=True
    )

    file_size = db.Column(
        db.Integer,
        nullable=True
    )

    image_width = db.Column(
        db.Integer,
        nullable=True
    )

    image_height = db.Column(
        db.Integer,
        nullable=True
    )

    quality_score = db.Column(
        db.Float,
        nullable=True
    )

    uploaded_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    case = db.relationship(
        "Case",
        back_populates="xray_images"
    )

    def __repr__(self):
        return f"<XRayImage {self.file_name}>"