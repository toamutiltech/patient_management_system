from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from patient import db, bcrypt
from patient.models import User, Apointment
from patient.apointments.forms import ApointmentForm
from patient.apointments.utils import save_picture

apointments = Blueprint('apointments', __name__)

#Route to submit the apointment form and redirect back to create apointment
@apointments.route("/apointment/new", methods=['GET', 'POST'])
@login_required
def new_apointment():
    form = ApointmentForm()
    if form.validate_on_submit():
        if form.image.data:
            image_file = save_picture(form.image.data)
            
        apointment = Apointment(title=form.title.data, description=form.description.data, size=form.size.data, location=form.location.data, country=form.country.data, image = image_file, price=form.price.data, space_type=form.space_type.data, availability=form.availability.data, facility=form.facility.data, contact=form.contact.data,  author=current_user)
        db.session.add(apointment)
        db.session.commit()
        flash('Your apointment has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_apointment.html', title='New Apointment',
                           form=form, legend='New Apointment')

#Route to view space apointment by the ID
@apointments.route("/apointment/<int:apointment_id>")
def apointment(apointment_id):
    apointment = Apointment.query.get_or_404(apointment_id)
    return render_template('apointment.html', title=apointment.title, apointment=apointment)

#Route to edit space apointment by the ID
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

#Route to delete space apointment by the ID
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

#Route to delete space apointment by the ID
@apointments.route('/apointment/search', methods=['GET'])
def search():
    selected_country = request.args.get('country')
    if selected_country:
        apointments = Apointment.query.filter_by(country=selected_country).all()
    else:
        apointments = []
    return render_template('search_results.html', apointments=apointments)

