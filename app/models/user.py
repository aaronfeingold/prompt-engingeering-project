from flask_bcrypt import Bcrypt
from datetime import datetime
from app.database import db
import re

bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    two_fa_setup = db.Column(db.Boolean, default=False)  # has the user set up 2FA?
    two_fa_secret = db.Column(db.String(32), nullable=True)  # Secret key for 2FA
    two_fa_backup_codes = db.Column(db.ARRAY(db.String), nullable=True)  # Backup codes
    roles = db.Column(db.ARRAY(db.Integer), nullable=False)
    teams = db.Column(db.ARRAY(db.Integer), nullable=True)
    regular_budget = db.Column(db.Integer, default=0)
    team_budgeted = db.Column(db.Boolean, default=False)
    temporary_budget = db.Column(db.Integer, default=0)
    temporary_budget_expiration = db.Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def validate_username(username):
        if re.match("^[a-zA-Z0-9]+[^_]$", username):
            return True
        return False
