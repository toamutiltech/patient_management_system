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
    medicals = db.relationship('Medical', backref='med', lazy=True)
    healths = db.relationship('Health', backref='worker', lazy=True)


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
    doctor = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
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
    all_records = db.relationship('Medical', backref='record', lazy=True)

    def __repr__(self):
        return f"Record('{self.patient_name}', '{self.date_posted}')"

class Medical(db.Model):
    med_id = db.Column(db.Integer, primary_key=True)
    allergies = db.Column(db.String(100), nullable=False)
    med_condition = db.Column(db.String(100), nullable=False)
    medication = db.Column(db.String(255), nullable=False)
    symptoms = db.Column(db.String(1000), nullable=False)
    surgerie = db.Column(db.String(255), nullable=False)
    doctor = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    record_id = db.Column(db.Integer, db.ForeignKey('record.user_id'), nullable=False)

    def __repr__(self):
        return f"Medical('{self.med_condition}', '{self.date_posted}')"

class Health(db.Model):
    worker_id = db.Column(db.Integer, primary_key=True)
    worker_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Health('{self.worker_name}', '{self.date_posted}')"