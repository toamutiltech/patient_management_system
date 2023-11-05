from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from patient.models import User

#The form to post space to the database
class ApointmentForm(FlaskForm):
    choices = [('Nike', 'Nike'), ('Mike', 'Mike'), 
    ('David', 'David')]
    doctor = SelectField('Select a Doctor', choices=choices)
    title = StringField('Title', validators=[DataRequired()])
    reason = StringField('Reason for Visit', validators=[DataRequired()])
    submit = SubmitField('Schedule Appointment')

#The form to Search space from the database
class SearchForm(FlaskForm):
    choices = [('Nike', 'Nike'), ('Mike', 'Mike'), 
    ('David', 'David')]
    doctor = SelectField('Select a Doctor', choices=choices)
    submit = SubmitField('Search')
    