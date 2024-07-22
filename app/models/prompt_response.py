import json
from app.database import db
from datetime import datetime


class PromptResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(
        db.Integer, db.ForeignKey("conversation.id"), nullable=True
    )
    messages = db.Column(db.Text, nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response_time = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<PromptResponse {self.id}>'

    @property
    def prompt_messages(self):
        """Deserialize the JSON string in the prompt column into Python objects."""
        return json.loads(self.prompt)

    @prompt_messages.setter
    def prompt_messages(self, messages):
        """Serialize the Python objects into a JSON string for storage in the prompt column."""
        self.prompt = json.dumps(messages)

    def to_dict(self):
        return {
            "id": self.id,
            "prompt": self.prompt_messages,
            "content": self.content,
            "role": self.role,
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
