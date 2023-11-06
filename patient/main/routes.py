from flask import render_template, request, Blueprint
from patient.models import Apointment, Medical
from flask_login import current_user, login_required
from patient.models import User, Record, Medical, Health
from patient import db 
from sqlalchemy import func
import pandas as pd

main = Blueprint('main', __name__)
"""
This route contain all first page loaded by the browser
"""
@main.route("/")
@main.route("/home")
def home():
	#Route to redirect to Home page where introduction of the site is made
	result = db.session.query(Medical.med_condition, func.count(Medical.med_condition)).group_by(
	          Medical.med_condition).all()
	df = pd.DataFrame(result, columns=['med_condition', 'count'])
	statistical_details = df.to_dict(orient='records')
	return render_template('home.html', title='Home', statistical_details=statistical_details)

@main.route("/view_apointment")
def view_apointment():
	#Route to redirect to Apointment page where Apointment booked will apear
	doctors = Health.query.with_entities(Health.worker_name).all()
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=current_user.username).first_or_404()
	apointments = Apointment.query.filter_by(author=user).order_by(Apointment.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('view_apointment.html', apointments=apointments, doctors=doctors)

@main.route("/about")
def about():
	#Route to redirect to about page when about is click or enter into the browser address
    return render_template('about.html', title='About')


@main.route("/contact")
def contact():
	#Route to redirect to Contact page when contact is click or enter into the browser address
    return render_template('contact.html', title='Contact')

@main.route("/worker")
def worker():
	#Route to redirect to Apointment page where Apointment booked will apear
	page = request.args.get('page', 1, type=int)
	apointments = Apointment.query.order_by(Apointment.date_posted.desc()).paginate(page=page, per_page=5)
	
	result = db.session.query(Medical.med_condition, func.count(Medical.med_condition)).group_by(
	          Medical.med_condition).all()
	df = pd.DataFrame(result, columns=['med_condition', 'count'])
	statistical_details = df.to_dict(orient='records')
	return render_template('worker_home.html', apointments=apointments, statistical_details=statistical_details)

@main.route("/myapointment")
def myapointment():
	#Route to redirect to Apointment page where Apointment booked will apear
	user = User.query.filter_by(username=current_user.username).first_or_404()
	patientapointment = Health.query.filter_by(worker=user).all()
	page = request.args.get('page', 1, type=int)
	apointments = Apointment.query.filter(Apointment.doctor.in_([doc.worker_name for doc in patientapointment]))\
        .order_by(Apointment.date_posted.desc())\
        .paginate(page=page, per_page=12)
	return render_template('myapointment.html', apointments=apointments)