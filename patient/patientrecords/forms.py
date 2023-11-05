from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, RadioField, PasswordField, DateField, SubmitField, BooleanField
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

class MedicalRecordForm(FlaskForm):
    allergies = StringField('What are Your Allergies',
                           validators=[DataRequired(), Length(min=3)])
    fever = RadioField('Do you Have Fever', choices=[('yes', 'I have'), ('no', 'I do not have')], validators=[DataRequired()])
    profuse_sweating = RadioField('Are Sweating Profusly', choices=[('yes', 'I Am'), ('no', 'I Am Not')], validators=[DataRequired()])
    headache = RadioField('Do you Have Headache', choices=[('yes', 'I have'), ('no', 'I do not have')], validators=[DataRequired()])
    nausea = RadioField('Do you Have nausea (A queasy sensation, feeling of loathing or disgust)', choices=[('yes', 'I have'), ('no', 'I do not have')], validators=[DataRequired()])
    vomiting = RadioField('Are you vomiting', choices=[('yes', 'I Am'), ('no', 'I Am Not')], validators=[DataRequired()])
    diarrhoea = RadioField('Do you Have diarrhoea ( Having loose, watery stools and stomach pain.)', choices=[('yes', 'I have'), ('no', 'I do not have')], validators=[DataRequired()])
    anaemia = RadioField('Do you Have anaemia (A lack of red blood cells Symptoms may include fatigue, skin pallor, shortness of breath, light-headedness, dizziness or a fast heartbeat.)', choices=[('yes', 'I have'), ('no', 'I do not have')], validators=[DataRequired()])
    submit = SubmitField('Submit Test Questions')

class HealthRecordForm(FlaskForm):
    worker_name = StringField('Full Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    gchoices = [('male', 'Male'), ('female', 'Female')]
    gender = SelectField('Select your Gender Type', choices=gchoices)
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    address = StringField('Full Address',
                           validators=[DataRequired()])
    submit = SubmitField('Update Your Record')


class UpdateHealthRecordForm(FlaskForm):
    worker_name = StringField('Full Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    address = StringField('Full Address',
                           validators=[DataRequired()])
    submit = SubmitField('Update')

class SearchHealthForm(FlaskForm):
    choices = [('Nike', 'Nike'), ('Mike', 'Mike'), 
    ('David', 'David')]
    doctor = SelectField('Select a Doctor', choices=choices)
    submit = SubmitField('Search Medical Condition')
