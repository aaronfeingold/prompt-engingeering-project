from app.database import db
from enum import Enum


class RoleEnum(Enum):
    USER = 1
    TEAM_LEADER = 2
    ADMIN = 3
    SUPER_ADMIN = 4


class UserRole(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(RoleEnum), unique=True)
