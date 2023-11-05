from flask import render_template, request, Blueprint
from patient.models import Apointment
from patient.models import User, Record, Medical, Health

main = Blueprint('main', __name__)
"""
This is the first page loaded by the browser,
It load with the space post available in the database 
it and redirect to home page when Home is click
"""
@main.route("/")
@main.route("/home")
def home():
    #Route to redirect to Home page where introduction of the site is made
    return render_template('home.html', title='Home')

@main.route("/view_apointment")
def view_apointment():
	#Route to redirect to Apointment page where Apointment booked will apear
	page = request.args.get('page', 1, type=int)
	apointments = Apointment.query.order_by(Apointment.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('view_apointment.html', apointments=apointments)

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
	return render_template('worker_home.html', apointments=apointments)

@main.route("/myapointment")
def myapointment():
	#Route to redirect to Apointment page where Apointment booked will apear
	page = request.args.get('page', 1, type=int)
	apointments = Apointment.query.order_by(Apointment.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('myapointment.html', apointments=apointments)
