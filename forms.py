from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class ConfirmDoseForm(FlaskForm):
    username = StringField("Your name", validators=[DataRequired(), Length(max=40)])
    taken = SubmitField("Taken")
    skipped = SubmitField("Skipped")
    remind_later = SubmitField("Remind me later")
