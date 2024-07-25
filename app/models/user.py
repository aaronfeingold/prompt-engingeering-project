from flask_bcrypt import Bcrypt
from datetime import datetime
from app.database import db
import re
from enum import Enum

bcrypt = Bcrypt()


class RoleEnum(Enum):
    USER = 1
    ADMIN = 2
    SUPER_ADMIN = 3


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    two_fa_setup = db.Column(db.Boolean, default=False)  # has the user set up 2FA?
    two_fa_secret = db.Column(db.String(32), nullable=True)  # Secret key for 2FA
    two_fa_backup_codes = db.Column(db.ARRAY(db.String), nullable=True)  # Backup codes
    role = db.Column(db.Enum(RoleEnum), nullable=False)
    teams = db.relationship("Team", secondary="teammates", back_populates="teammates")
    leading_teams = db.relationship(
        "Team", secondary="team_leaders", back_populates="leaders"
    )
    usages = db.relationship("OpenAIUsage", back_populates="user")
    prompt_responses = db.relationship("PromptResponse", back_populates="user")
    regular_budget = db.Column(db.Integer, default=0)
    team_budgeted = db.Column(db.Boolean, default=False)
    temporary_budget = db.Column(db.Integer, default=0)
    temporary_budget_expiration = db.Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def set_password(self, password):
        if not self.validate_password(password):
            raise ValueError("Password must be between 8-20 characters.")
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def validate_username(username):
        if re.match("^[a-zA-Z0-9]+[^_]$", username):
            return True
        return False

    @staticmethod
    def validate_password(password):
        return 8 <= len(password) <= 20

    def is_on_team(self, team_id):
        return any(team.id == team_id for team in self.teams)
