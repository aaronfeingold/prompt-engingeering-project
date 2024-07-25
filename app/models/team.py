from app.database import db


class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key=True)
    teammates = db.Column(db.ARRAY(db.Integer), nullable=True)
    team_leaders = db.Column(db.ARRAY(db.Integer), nullable=True)
    team_size = db.Column(db.Integer, default=0)
    regular_budget = db.Column(db.Integer, default=0)
    temporary_budget = db.Column(db.Integer, default=0)
    temporary_budget_expiration = db.Column(db.DateTime, nullable=True)
    team_size_limit = db.Column(db.Integer, default=10)
