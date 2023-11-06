from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from patient import db, bcrypt
from patient.models import User, Apointment, Record, Medical, Health
from patient.apointments.forms import ApointmentForm
from patient.apointments.utils import save_picture

apointments = Blueprint('apointments', __name__)

#Route to submit the apointment form and redirect back to create apointment
@apointments.route("/apointment/new", methods=['GET', 'POST'])
@login_required
def new_apointment():
    doctors = Health.query.with_entities(Health.worker_name).all()
    form = ApointmentForm()
    if request.method == 'POST':
        apointment = Apointment(title=form.title.data, doctor=form.doctor.data, reason=form.reason.data, author=current_user)
        db.session.add(apointment)
        db.session.commit()       
        flash('Your apointment has been created!', 'success')
        return redirect(url_for('main.view_apointment'))
    return render_template('create_apointment.html', title='New Apointment',
                           form=form, legend='New Apointment', doctors=doctors)

#Route to view apointment by the ID
@apointments.route("/apointment/<int:apointment_id>")
def apointment(apointment_id):
    apointment = Apointment.query.get_or_404(apointment_id)
    return render_template('apointment.html', title=apointment.title, apointment=apointment)

#Route to view apointment by the ID for Health Workers
@apointments.route("/apointmentstatus/<int:apointment_id>")
def status(apointment_id):
    apointment = Apointment.query.get_or_404(apointment_id)
    medicals = Medical.query.first_or_404()
    return render_template('apointment_status.html', title=apointment.title, apointment=apointment, medicals=medicals)

#Route to edit apointment by the ID
@apointments.route("/apointment/<int:apointment_id>/update", methods=['GET', 'POST'])
@login_required
def update_apointment(apointment_id):
    apointment = Apointment.query.get_or_404(apointment_id)
    if apointment.author != current_user:
        abort(403)
    form = ApointmentForm()
    if form.validate_on_submit():
        apointment.title = form.title.data
        apointment.content = form.content.data
        db.session.commit()
        flash('Your apointment has been updated!', 'success')
        return redirect(url_for('apointments.apointment', apointment_id=apointment.id))
    elif request.method == 'GET':
        form.title.data = apointment.title
        form.content.data = apointment.content
    return render_template('create_apointment.html', title='Update Apointment',
                           form=form, legend='Update Apointment')

#Route to view apointment by the ID for Health Workers and answer the apointment
@apointments.route("/apointment/update", methods=['GET', 'POST'])
@login_required
def ans_apointment():    
    if request.method == 'POST':
        apointment_id = request.form.get('apointment_id')
        apointment = Apointment.query.get_or_404(apointment_id)
        medicals = Medical.query.first_or_404()
        if 'accept' in request.form:
            apointment.date = request.form.get('date')
            apointment.time = request.form.get('time')
            apointment.status = 'accept'
        elif 'reject' in request.form:
            apointment.status = 'reject'

        db.session.commit()
        flash('The appointment has been updated!', 'success')
        return redirect(url_for('apointments.status', apointment_id=apointment_id)) 
    return render_template('apointment_status.html', title=apointment.title, apointment=apointment, medicals=medicals)

#Route to delete apointment by the ID
@apointments.route("/apointment/<int:apointment_id>/delete", methods=['POST'])
@login_required
def delete_apointment(apointment_id):
    apointment = Apointment.query.get_or_404(apointment_id)
    if apointment.author != current_user:
        abort(403)
    db.session.delete(apointment)
    db.session.commit()
    flash('Your apointment has been deleted!', 'success')
    return redirect(url_for('main.home'))

#Route to search doctor to book apointment
@apointments.route('/apointment/search', methods=['GET'])
def search():
    selected_doctor = request.args.get('doctor')
    if selected_doctor:
        doctors = selected_doctor
    else:
        doctors = []
    return render_template('search_results.html', doctors=doctors)

