from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from patient import db, bcrypt
from patient.models import User, Record
from patient.patientrecords.forms import (PatientRecordForm, UpdatePatientRecordForm)

patientrecords = Blueprint('patientrecords', __name__)

# Route to submit the Patient Record form and redirect back to Patient Record
@patientrecords.route("/update_patientrecord", methods=['GET', 'POST'])
@login_required
def update_patientrecord():
    form = PatientRecordForm()
    if form.validate_on_submit():   
        record = Record(patient_name=form.patient_name.data, gender=form.gender.data, dob=form.dob.data, address=form.address.data, emergency_name=form.emergency_name.data, emergency_relationship = form.emergency_relationship.data, emergency_phone=form.emergency_phone.data, record=current_user)
        db.session.add(record)
        db.session.commit()
        flash('You have updated your record!', 'success')
        return redirect(url_for('main.home'))
    return render_template('patient_record.html', title='Update Patient Record',
                           form=form, legend='Update Patient Record')

@patientrecords.route("/myrecord", methods=['GET', 'POST'])
@login_required
def myrecord():
     user = User.query.filter_by(username=current_user.username).first_or_404()
     patientrecords = Record.query.filter_by(user=user).all()
     for record in patientrecords:
        form = UpdatePatientRecordForm()
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('users.account'))
        else:
            form.patient_name.data = record.patient_name
            form.address.data = record.address
            form.emergency_name.data = record.emergency_name
            form.emergency_relationship.data = record.emergency_relationship
            form.emergency_phone.data = record.emergency_phone
        return render_template('myrecord.html', title='my Record', patientrecords=patientrecords,
                            user=user, form=form)

#Route to edit space apointment by the ID
"""@apointments.route("/patient_record/<int:patient_id>/update", methods=['GET', 'POST'])
@login_required
def update_patient_record(patient_id):
    patient_record = Record.query.get_or_404(patient_id)
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
"""
