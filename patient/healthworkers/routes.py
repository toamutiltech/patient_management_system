from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from patient import db, bcrypt
from patient.models import User, Record, Medical, Health
from patient.healthworkers.forms import (HealthRecordForm, UpdateHealthRecordForm)
import json
 
healthworkers = Blueprint('healthworkers', __name__)

#Health Worker Home page
@healthworkers.route("/home")
@login_required
def workerhome():
    #Route to redirect to Apointment page where Apointment booked will apear
    page = request.args.get('page', 1, type=int)
    apointments = Apointment.query.order_by(Apointment.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('worker_home.html', apointments=apointments)

# Route to submit the Health Worker Record form and redirect back to Worker Record
@healthworkers.route("/update_workerrecord", methods=['GET', 'POST'])
@login_required
def update_workerrecord():
    form = HealthRecordForm()
    if form.validate_on_submit():   
        health = Health(worker_name=form.worker_name.data, gender=form.gender.data, dob=form.dob.data, address=form.address.data, worker=current_user)
        db.session.add(health)
        db.session.commit()
        flash('You have updated your record!', 'success')
        return redirect(url_for('healthworkers.workerrecord'))
    return render_template('worker_record.html', title='Update Worker Record',
                           form=form, legend='Update Worker Record')

# Route to Health Worker Record
@healthworkers.route("/workerrecord", methods=['GET', 'POST'])
@login_required
def workerrecord():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    healthworkers = Health.query.filter_by(worker=user).all()
    if not healthworkers:  # Checking if healthworker list is empty
        return redirect(url_for('healthworkers.update_workerrecord'))
    else:
        form = UpdateHealthRecordForm()
        if request.method == 'POST':
            for record in healthworkers:
                record.worker_name = form.worker_name.data
                record.address = form.address.data
                try:
                    db.session.add(record)  # Add the updated record to the session
                    db.session.commit()  # Commit the changes
                    flash('Your account has been updated!', 'success')
                    return redirect(url_for('healthworkers.workerrecord'))
                except Exception as e:
                    flash(f'An error occurred: {e}', 'error')
                    db.session.rollback()  # Roll back changes if an error occurs
        else:
            for record in healthworkers:
                form.worker_name.data = record.worker_name
                form.address.data = record.address
        return render_template('healthworker.html', title='My Record', healthworkers=healthworkers, user=user, form=form)
