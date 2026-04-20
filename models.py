from datetime import datetime, time
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db


class User(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(63), unique=True, index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(119), unique=True, index=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))

    schedules: so.Mapped[list["MedicationSchedule"]] = so.relationship(back_populates="user")
    reminders: so.Mapped[list["ReminderPrompt"]] = so.relationship(back_populates="user")
    notifications: so.Mapped[list["ReminderNotification"]] = so.relationship(back_populates="user")
    dose_logs: so.Mapped[list["DoseLog"]] = so.relationship(back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class MedicationSchedule(db.Model):
    __tablename__ = "medication_schedule"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), index=True)
    med_name: so.Mapped[str] = so.mapped_column(sa.String(80))
    dosage: so.Mapped[str] = so.mapped_column(sa.String(80))
    scheduled_time: so.Mapped[time] = so.mapped_column(sa.Time())
    email: so.Mapped[Optional[str]] = so.mapped_column(sa.String(119), nullable=True)
    active: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=True)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(), default=datetime.now)
    updated_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(), default=datetime.now, onupdate=datetime.now)

    user: so.Mapped[User] = so.relationship(back_populates="schedules")
    reminders: so.Mapped[list["ReminderPrompt"]] = so.relationship(back_populates="schedule", cascade="all, delete-orphan")
    dose_logs: so.Mapped[list["DoseLog"]] = so.relationship(back_populates="schedule", cascade="all, delete-orphan")


class ReminderPrompt(db.Model):
    __tablename__ = "reminder_prompt"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), index=True)
    schedule_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("medication_schedule.id"), index=True)
    parent_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("reminder_prompt.id"), nullable=True)
    dose_date: so.Mapped[str] = so.mapped_column(sa.String(10), index=True)
    stage: so.Mapped[str] = so.mapped_column(sa.String(20))
    status: so.Mapped[str] = so.mapped_column(sa.String(20), index=True)
    due_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(), index=True)
    original_due_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime())
    expires_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime())
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(), default=datetime.now)
    responded_at: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime(), nullable=True)
    email_sent_at: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime(), nullable=True)

    user: so.Mapped[User] = so.relationship(back_populates="reminders")
    schedule: so.Mapped[MedicationSchedule] = so.relationship(back_populates="reminders")
    parent: so.Mapped[Optional["ReminderPrompt"]] = so.relationship(remote_side=[id])
    notifications: so.Mapped[list["ReminderNotification"]] = so.relationship(back_populates="reminder", cascade="all, delete-orphan")

    __table_args__ = (
        sa.UniqueConstraint("schedule_id", "dose_date", "stage", name="uq_schedule_dose_stage"),
    )


class ReminderNotification(db.Model):
    __tablename__ = "reminder_notification"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), index=True)
    reminder_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("reminder_prompt.id"), index=True)
    channel: so.Mapped[str] = so.mapped_column(sa.String(20))
    message: so.Mapped[str] = so.mapped_column(sa.String(255))
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(), default=datetime.now, index=True)

    user: so.Mapped[User] = so.relationship(back_populates="notifications")
    reminder: so.Mapped[ReminderPrompt] = so.relationship(back_populates="notifications")


class DoseLog(db.Model):
    __tablename__ = "dose_log"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), index=True)
    schedule_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("medication_schedule.id"), index=True)
    reminder_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("reminder_prompt.id"), nullable=True)
    dose_date: so.Mapped[str] = so.mapped_column(sa.String(10), index=True)
    scheduled_for: so.Mapped[datetime] = so.mapped_column(sa.DateTime())
    logged_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(), default=datetime.now, index=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(20))

    user: so.Mapped[User] = so.relationship(back_populates="dose_logs")
    schedule: so.Mapped[MedicationSchedule] = so.relationship(back_populates="dose_logs")

    __table_args__ = (
        sa.UniqueConstraint("user_id", "schedule_id", "dose_date", name="uq_user_schedule_dose_date"),
    )


