from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from patient.models import User

#The form to post space to the database
class ApointmentForm(FlaskForm):
    choices = [('Nigeria', 'Nigeria'), ('Argentina', 'Argentina'), 
    ('Algeria', 'Algeria'), ('Benin', 'Benin'),('Brazil', 'Brazil'), 
    ('Cuba', 'Cuba'),('United States', 'United States'),('United Kingdom', 'United Kingdom'),
    ('Togo', 'Togo'),('South Africa', 'South Africa'),('Portugal', 'Portugal')
    ]
    country = SelectField('Select a Country', choices=choices)
    title = StringField('Title', validators=[DataRequired()])
    image = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    size = StringField('Size', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    space_type = StringField('Space Type', validators=[DataRequired()])
    availability = StringField('Availability', validators=[DataRequired()])
    facility = TextAreaField('Facility', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    contact = TextAreaField('Contact', validators=[DataRequired()])
    submit = SubmitField('Post')

#The form to Search space from the database
class SearchForm(FlaskForm):
    choices = [('Nigeria', 'Nigeria'), ('Argentina', 'Argentina'), 
    ('Algeria', 'Algeria'), ('Benin', 'Benin'),('Brazil', 'Brazil'), 
    ('Cuba', 'Cuba'),('United States', 'United States'),('United Kingdom', 'United Kingdom'),
    ('Togo', 'Togo'),('South Africa', 'South Africa'),('Portugal', 'Portugal')]
    country = SelectField('Select a Country', choices=choices)
    submit = SubmitField('Post')