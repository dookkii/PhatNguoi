from flask import Blueprint
from flask import url_for
from flask import request
from flask_login import login_user
from flask_login import logout_user
from json import loads, dumps
from arrow import utcnow
from authlib.integrations.base_client.errors import MismatchingStateError

from helpers.api_key import generate_api_key
from helpers.flask_utility import TomChienXuOJ_redirect as redirect
from helpers.url import clean_google_avatar_image_url

from models import User

from .. import database
from .. import google_oauth2

blueprint = Blueprint("authentication", __name__)

oauth2_google_blueprint = Blueprint("oauth2_google", __name__, url_prefix="/oauth2-google")
blueprint.register_blueprint(oauth2_google_blueprint)

@blueprint.route("/logout")
def logout():
  logout_user()
  return redirect(url_for("main.homepage"))

@oauth2_google_blueprint.route("/login")
def oauth2_google_login():
  redirect_uri = url_for("authentication.oauth2_google.oauth2_google_authorize", _external=True)
  return google_oauth2.authorize_redirect(redirect_uri)

@oauth2_google_blueprint.route("/authorize")
def oauth2_google_authorize():
  try:
    user_info_endpoint = google_oauth2.server_metadata["userinfo_endpoint"]
  
    token = google_oauth2.authorize_access_token()
    user_info = loads(dumps(google_oauth2.get(user_info_endpoint).json()))
    email = user_info.get("email")

    user = User.query.filter_by(email=email).first()
    if user is None:
      new_user = User(
        email=email,
        name=user_info.get("name"),
        oauth2_token=token.get("access_token"),
        avatar_url=clean_google_avatar_image_url(user_info.get("picture")),
        api_key=generate_api_key(prefix="tomchienxu_", suffix="_phatnguoi-api"),
      )
      database.session.add(new_user)
      
      user = new_user
    else: 
      user.token = token.get("access_token")

    user.last_login = utcnow().datetime
    user.last_ip = request.remote_addr
    database.session.commit()
    
    login_user(user)
    return redirect(url_for("main.homepage"))
  except MismatchingStateError:
    return redirect(url_for("main.homepage"))
  except Exception as error:
    return redirect(url_for("main.homepage"))