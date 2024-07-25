from app.database import db

# Define the association tables
teammates = db.Table(
    "teammates",
    db.Column("team_id", db.Integer, db.ForeignKey("teams.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
)

team_leaders = db.Table(
    "team_leaders",
    db.Column("team_id", db.Integer, db.ForeignKey("teams.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
)


class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key=True)
    teammates = db.relationship("User", secondary=teammates, back_populates="teams")
    team_leaders = db.relationship(
        "User", secondary=team_leaders, back_populates="leading_teams"
    )
    usages = db.relationship("OpenAIUsage", back_populates="team")
    team_size = db.Column(db.Integer, default=0)
    regular_budget = db.Column(db.Integer, default=0)
    temporary_budget = db.Column(db.Integer, default=0)
    temporary_budget_expiration = db.Column(db.DateTime, nullable=True)
    team_size_limit = db.Column(db.Integer, default=10)
