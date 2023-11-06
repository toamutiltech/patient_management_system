from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, RadioField, PasswordField, DateField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from patient.models import User
 
#Health Worker Record Form 
class HealthRecordForm(FlaskForm):
    worker_name = StringField('Full Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    gchoices = [('male', 'Male'), ('female', 'Female')]
    gender = SelectField('Select your Gender Type', choices=gchoices)
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    address = StringField('Full Address',
                           validators=[DataRequired()])
    submit = SubmitField('Update Your Record')

#Health Worker Updating Record Form 
class UpdateHealthRecordForm(FlaskForm):
    worker_name = StringField('Full Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    address = StringField('Full Address',
                           validators=[DataRequired()])
    submit = SubmitField('Update')


