from datetime import datetime
from flask import current_app
from patient import db, login_manager
from flask_login import UserMixin

#fuction to load a login user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#users class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    user_type = db.Column(db.String(20), unique=True, nullable=False)
    apointments = db.relationship('Apointment', backref='author', lazy=True)
    patientrecords = db.relationship('Record', backref='record', lazy=True)
    records = db.relationship('Record', backref='user', lazy='dynamic')


    #fuction for reset code to reset password
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

     #fuction for verifing code to reset password   
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

#Apointment table model
class Apointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    size = db.Column(db.String(100), nullable=False)
    space_type = db.Column(db.String(255), nullable=False)
    accommodation_size = db.Column(db.String(100), nullable=False)
    facility = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.Text, nullable=False)
    availability = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(100), nullable=False, default='default.jpg')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Apointment('{self.title}', '{self.date_posted}')"

class Record(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    emergency_name = db.Column(db.String(100), nullable=False)
    emergency_relationship = db.Column(db.String(255), nullable=False)
    emergency_phone = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Patient('{self.name}', '{self.date_posted}')"

