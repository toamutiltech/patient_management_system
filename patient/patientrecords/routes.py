from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from patient import db, bcrypt
from patient.models import User, Record, Medical
from patient.patientrecords.forms import (PatientRecordForm, UpdatePatientRecordForm, MedicalRecordForm)
import json

#This route contain all route to the Patient, Medical and Health Records

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
        return redirect(url_for('patientrecords.myrecord'))
    return render_template('patient_record.html', title='Update Patient Record',
                           form=form, legend='Update Patient Record')

@patientrecords.route("/myrecord", methods=['GET', 'POST'])
@login_required
def myrecord():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    patientrecords = Record.query.filter_by(user=user).all()
    if not patientrecords:  # Checking if patientrecords list is empty
        return redirect(url_for('patientrecords.update_patientrecord'))
    else:
        form = UpdatePatientRecordForm()
        if request.method == 'POST':
            for record in patientrecords:
                record.patient_name = form.patient_name.data
                record.address = form.address.data
                record.emergency_name = form.emergency_name.data
                record.emergency_relationship = form.emergency_relationship.data
                record.emergency_phone = form.emergency_phone.data
                try:
                    db.session.add(record)  # Add the updated record to the session
                    db.session.commit()  # Commit the changes
                    flash('Your account has been updated!', 'success')
                    return redirect(url_for('patientrecords.myrecord'))
                except Exception as e:
                    flash(f'An error occurred: {e}', 'error')
                    db.session.rollback()  # Roll back changes if an error occurs
        else:
            for record in patientrecords:
                form.patient_name.data = record.patient_name
                form.address.data = record.address
                form.emergency_name.data = record.emergency_name
                form.emergency_relationship.data = record.emergency_relationship
                form.emergency_phone.data = record.emergency_phone
        return render_template('myrecord.html', title='My Record', patientrecords=patientrecords, user=user, form=form)

@patientrecords.route("/medicalrecord/new", methods=['GET', 'POST'])
@login_required
def new_medicalrecord():
    form = MedicalRecordForm()
    if form.validate_on_submit(): 
        fever = request.form['fever']
        headache = request.form['headache']
        profuse_sweating = request.form['profuse_sweating']
        nausea = request.form['nausea']
        vomiting = request.form['vomiting']
        diarrhoea = request.form['diarrhoea']
        anaemia = request.form['anaemia']

        symptoms = {}
        symptoms['fever'] = request.form['fever']
        symptoms['headache'] = request.form['headache']
        symptoms['profuse_sweating'] = request.form['profuse_sweating']
        symptoms['nausea'] = request.form['nausea']
        symptoms['vomiting'] = request.form['vomiting']
        symptoms['diarrhoea'] = request.form['diarrhoea']
        symptoms['anaemia'] = request.form['anaemia']
        symptoms_json = json.dumps(symptoms)

        if fever == headache == profuse_sweating == nausea == vomiting == diarrhoea == anaemia == 'yes':
            result = 'You have Malaria.'
            med_condition = 'Malaria'
            medical = Medical(
            allergies=form.allergies.data,
            symptoms=symptoms_json,
            med_condition=med_condition,
            user_id=current_user.id,  # Replace with the appropriate value
            record_id=current_user.id  # Replace with the appropriate value
            )

            db.session.add(medical)
            db.session.commit()           
        else:
            result = 'You do not have any Illness.' 
            return render_template('medicalrecord.html', title='Medical Record',
                           form=form, result=result, legend='Medical Record')
        flash('You have You have fill up a Medical Record!', 'success')
        return redirect(url_for('patientrecords.medicalrecord'))
    return render_template('medicalrecord.html', title='Medical Record',
                           form=form, legend='Medical Record')

@patientrecords.route("/medicalrecords")
@login_required
def medicalrecord():
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    medicals = Medical.query.filter_by(med=user).order_by(Medical.date_posted.desc()).paginate(page=page, per_page=3)
    symptoms_dict = {}
    for medical in medicals:
        if medical.symptoms:
            symptoms_dict = json.loads(medical.symptoms)
    return render_template('medrecords.html', title='My Medical Records', medicals=medicals, symptoms=symptoms_dict, user=user)


@patientrecords.route("/allrecords")
@login_required
def allmedicalrecord():
    page = request.args.get('page', 1, type=int)
    medicals = Medical.query.order_by(Medical.date_posted.desc()).paginate(page=page, per_page=12)
    distinct_conditions = db.session.query(Medical.med_condition).distinct().all()
    symptoms_dict = {}
    for medical in medicals:
        if medical.symptoms:
            symptoms_dict = json.loads(medical.symptoms)
    return render_template('all_medical_record.html', medicals=medicals, symptoms=symptoms_dict, distinct_conditions=distinct_conditions)

@patientrecords.route("/userrecords")
@login_required
def userrecords():
    page = request.args.get('page', 1, type=int)
    medicals = Medical.query.order_by(Medical.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('users_records.html', medicals=medicals)

@patientrecords.route("/record/<string:med_id>")
def user_record(med_id):
    medicals = Medical.query.filter_by(med_id=med_id)
    symptoms_dict = {}
    for medical in medicals:
        if medical.symptoms:
            symptoms_dict = json.loads(medical.symptoms)
    return render_template('view_record.html', medicals=medicals, symptoms=symptoms_dict)

#Route 
@patientrecords.route('/medical/search', methods=['GET'])
def medsearch():
    page = request.args.get('page', 1, type=int)
    distinct_conditions = db.session.query(Medical.med_condition).distinct().all()
    selected_illness = request.args.get('med_condition')
    if selected_illness:
        medicals = Medical.query.filter_by(med_condition=selected_illness).order_by(Medical.date_posted.desc()).paginate(page=page, per_page=6)
    else:
        medicals = []
    return render_template('search_condition.html', medicals=medicals, distinct_conditions=distinct_conditions)
