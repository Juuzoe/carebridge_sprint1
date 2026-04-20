from extensions import db
import sqlalchemy.orm as so
import sqlalchemy as sa
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(63), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(119), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Schedule(db.Model):
    __tablename__ = "schedule"

    id = db.Column(db.Integer, primary_key=True)
    med_name = db.Column(db.String(80), nullable=False)
    dosage = db.Column(db.String(80), nullable=False)

    # Must be stored as HH:MM, e.g. "08:00", "20:30"
    time_of_day = db.Column(db.String(5), nullable=False)


class DoseLog(db.Model):
    __tablename__ = "dose_log"

    id = db.Column(db.Integer, primary_key=True)
    when = db.Column(db.DateTime, nullable=False)
    day = db.Column(db.String(10), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey("schedule.id"), nullable=False, index=True)
    username = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    schedule = db.relationship("Schedule", backref="dose_logs")


DEFAULT_SCHEDULES = [
    {"med_name": "Aspirin", "dosage": "1 tablet", "time_of_day": "08:00"},
    {"med_name": "Vitamin D", "dosage": "1 capsule", "time_of_day": "20:00"},
]


def seed_schedules():
    for row in DEFAULT_SCHEDULES:
        db.session.add(Schedule(**row))
