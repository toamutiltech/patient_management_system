from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, PasswordField, DateField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from patient.models import User


class PatientRecordForm(FlaskForm):
    patient_name = StringField('Full Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    gchoices = [('male', 'Male'), ('female', 'Female')]
    gender = SelectField('Select your Gender Type', choices=gchoices)
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    address = StringField('Full Address',
                           validators=[DataRequired()])
    emergency_name = StringField('Emergency Contact Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    emergency_phone = StringField('Emergency Contact Phone Number',
                           validators=[DataRequired(), Length(min=2, max=100)])
    emergency_relationship = StringField('Relationship',
                           validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Update Your Record')


class UpdatePatientRecordForm(FlaskForm):
    patient_name = StringField('Full Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    gchoices = [('male', 'Male'), ('female', 'Female')]
    gender = SelectField('Select your Gender Type', choices=gchoices)
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    address = StringField('Full Address',
                           validators=[DataRequired()])
    emergency_name = StringField('Emergency Contact Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    emergency_phone = StringField('Emergency Contact Phone Number',
                           validators=[DataRequired(), Length(min=2, max=100)])
    emergency_relationship = StringField('Relationship',
                           validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Update')
