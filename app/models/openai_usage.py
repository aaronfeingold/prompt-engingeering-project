from app.database import db
from datetime import datetime


class OpenAIUsage(db.Model):
    __tablename__ = "openai_usage"
    id = db.Column(db.Integer, primary_key=True)
    prompt_response_id = db.Column(
        db.Integer, db.ForeignKey("prompt_response.id"), nullable=False
    )
    completion_tokens = db.Column(db.Integer, nullable=False)
    prompt_tokens = db.Column(db.Integer, nullable=False)
    total_tokens = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def add_to_db(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Insertion to the OpenAIUsage table failed: {e}")
