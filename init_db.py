import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize the Flask app
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patient_site.db'  # Replace with your database URI

# Initialize SQLAlchemy and Migrate extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import your models here
from patient.models import User, Apointment, Record, Medical, Health  # Replace 'your_app' with your actual app package name

if __name__ == '__main__':
    # Create the database tables
    with app.app_context():
        db.create_all()
