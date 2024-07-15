from app.database import db
from datetime import datetime


class PromptResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    response_time = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<PromptResponse {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'prompt': self.prompt,
            'content': self.content,
            'role': self.role,
            'response_time': self.response_time,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def add_to_db(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
