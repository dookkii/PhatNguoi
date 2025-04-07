from flask import Blueprint
from flask import request
from flask import url_for

from helpers.flask_utility import TomChienXuOJ_redirect as redirect
from helpers.flask_utility import TomChienXuOJ_render_template as render_template
from helpers.custom_thread import TomChienXuOJThread
from handlers.violation import safely_get_violations

blueprint = Blueprint("main_blueprint", __name__)

@blueprint.route("/", methods=["GET", "POST"])
def homepage():
  if request.method == "POST":
    bien_so_xe = request.form.get("bien-so-xe")
    loai_xe = request.form.get("loai-xe")

    if not all([bien_so_xe, loai_xe]):
      return redirect(url_for("main_blueprint.homepage"))
    
    thread = TomChienXuOJThread(target=safely_get_violations, args=(bien_so_xe, loai_xe))
    thread.start()
    data = thread.join(timeout=10)

    if thread.is_alive():
      thread.join()
    
    if data is None:
      return render_template("view/result.html", data=data)

    if data.get("violations") is None:
      return render_template("view/result.html", data=data)
    
    data["total"] = len(data["violations"])
    data["number_of_unpaid"] = 0

    for violation in data.get("violations"):
      if violation.get("trang_thai") == "Chưa xử phạt":
        data["number_of_unpaid"] += 1

    data["number_of_paid"] = data["total"] - data["number_of_unpaid"]

    return render_template("view/result.html", data=data)

  return render_template("view/homepage.html")