from datetime import datetime, timezone

from app.extensions import db


class AIAnalysis(db.Model):
    __tablename__ = "ai_analyses"

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

    model_name = db.Column(
        db.String(150),
        nullable=False
    )

    model_version = db.Column(
        db.String(100),
        nullable=True
    )

    prediction = db.Column(
        db.String(200),
        nullable=True
    )

    confidence = db.Column(
        db.Float,
        nullable=True
    )

    explanation = db.Column(
        db.Text,
        nullable=True
    )

    gradcam_path = db.Column(
        db.String(500),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    case = db.relationship(
        "Case",
        back_populates="ai_analyses"
    )

    def __repr__(self):
        return f"<AIAnalysis {self.id}>"