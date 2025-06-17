from flask import Blueprint
from flask import request
from flask_login import current_user

from helpers.flask_utility import TomChienXuOJ_redirect as redirect
from helpers.flask_utility import TomChienXuOJ_render_template as render_template
from helpers.custom_thread import TomChienXuOJThread
from handlers.violation import safely_get_violations

from settings import USE_RECAPTCHA

from forms import ViolationLookupForm
from forms import ViolationLookupFormWithRecaptcha

blueprint = Blueprint("main", __name__)

# TomChienXu Note: This is used for serving static files in Flask
# when using subdomains, also for supporting static file of nginx.
@blueprint.route("/static/<path:filename>")
def static(filename):
  return redirect(f"/static/{filename}")

@blueprint.route("/", methods=["GET", "POST"])
def homepage():
  if USE_RECAPTCHA:
    form = ViolationLookupFormWithRecaptcha()
  else:
    form = ViolationLookupForm()

  if "submit_my_number_plate" in request.form:
    form.is_my_plate = True

  if form.validate_on_submit():
    if "submit_my_number_plate" not in request.form:
      bien_so_xe = form.number_plate.data
      loai_xe = form.vehicle_type.data
    else:
      bien_so_xe = current_user.number_plate
      loai_xe = str(current_user.vehicle_type)
      
    thread = TomChienXuOJThread(target=safely_get_violations, args=(bien_so_xe, loai_xe))
    thread.start()
    data = thread.join(timeout=10)

    if thread.is_alive():
      thread.join()
    
    if data is None:
      return render_template("view/violation_lookup/result.html", data=data)

    if data.get("violations") is None:
      return render_template("view/violation_lookup/result.html", data=data)
    
    data["total"] = len(data["violations"])
    data["number_of_unpaid"] = 0

    for violation in data.get("violations"):
      if violation.get("trang_thai") == "Chưa xử phạt":
        data["number_of_unpaid"] += 1

    data["number_of_paid"] = data["total"] - data["number_of_unpaid"]

    return render_template("view/violation_lookup/result.html", data=data)

  fields = [
    form.number_plate,
    form.vehicle_type,
  ]
  if USE_RECAPTCHA:
    fields.append(form.recaptcha)
    
  errors = {
    field.label: field.errors for field in fields if field.errors
  }

  return render_template("view/violation_lookup/homepage.html", form=form, errors=errors)