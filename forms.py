import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError

from extensions import db
from models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=63)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=119)])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password",
        validators=[DataRequired(), EqualTo("password")],
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data.strip()))
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data.strip()))
        if user is not None:
            raise ValidationError("Please use a different email address.")


class MedicationForm(FlaskForm):
    med_name = StringField("Medication", validators=[DataRequired(), Length(max=80)])
    dosage = StringField("Dosage", validators=[DataRequired(), Length(max=80)])
    scheduled_time = TimeField("Scheduled time", format="%H:%M", validators=[DataRequired()])
    email = StringField("Notification email", validators=[Optional(), Email(), Length(max=119)])
    active = BooleanField("Active", default=True)
    submit = SubmitField("Save")

