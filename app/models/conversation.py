from app.database import db
from datetime import datetime


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    prompt_responses = db.relationship(
        "PromptResponse", backref="conversation", lazy=True
    )

    def __repr__(self):
        return f"<Conversation {self.id}>"
