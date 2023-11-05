from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from patient.config import Config
from sqlalchemy import func

 
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patient_site.db'
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    with app.app_context():
        db.create_all()  # Create database tables

    from patient.users.routes import users
    from patient.apointments.routes import apointments
    from patient.main.routes import main
    from patient.patientrecords.routes import patientrecords
    from patient.healthworkers.routes import healthworkers
    from patient.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(apointments)
    app.register_blueprint(main)
    app.register_blueprint(patientrecords)
    app.register_blueprint(healthworkers)
    app.register_blueprint(errors)

    return app
