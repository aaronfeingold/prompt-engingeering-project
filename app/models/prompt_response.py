from app.database import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB


class PromptResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(
        db.Integer, db.ForeignKey("conversation.id"), nullable=True
    )
    responses = db.Column(JSONB, nullable=False)
    prompts = db.Column(JSONB, nullable=False)
    response_time = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PromptResponse {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "prompts": self.prompts,
            "responses": self.responses,
            "response_time": self.response_time,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def add_to_db(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Insertion to the database failed: {e}")
