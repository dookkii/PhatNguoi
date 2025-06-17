from .. import database
from .. import render_template
from .. import redirect

from settings import USE_RECAPTCHA

from models import User

from forms import UserNumberPlate
from forms import UserNumberPlateWithRecaptcha

from flask import url_for
from flask import Blueprint
from flask_login import current_user
from flask_login import login_required

blueprint = Blueprint("profile", __name__)

@blueprint.route("/")
@login_required
def index():
  return redirect(url_for("profile.my_profile"))

@blueprint.route("/me")
@login_required
def my_profile():
  return render_template("view/profile/profile.html")

@blueprint.route("/mynumberplate", methods=["GET", "POST"])
@login_required
def my_number_plate():
  if USE_RECAPTCHA:
    form = UserNumberPlateWithRecaptcha()
  else:
    form = UserNumberPlate()

  if form.validate_on_submit():
    user = User.query.get(current_user.id)
    user.number_plate = form.number_plate.data
    user.vehicle_type = form.vehicle_type.data

    database.session.commit()
    
    return render_template("view/profile/number_plate.html", form=form, success=True)

  fields = [
    form.number_plate,
    form.vehicle_type,
  ]
  if USE_RECAPTCHA:
    fields.append(form.recaptcha)
    
  errors = {
    field.label: field.errors for field in fields if field.errors
  }
  return render_template("view/profile/number_plate.html", form=form, errors=errors)
