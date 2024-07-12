from app import db
from datetime import datetime

class PromptResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String, nullable=False)
    response = db.Column(db.String, nullable=False)
    response_time = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<PromptResponse {self.id}>'
