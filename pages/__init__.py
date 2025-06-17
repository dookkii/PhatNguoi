from dotenv import load_dotenv
from os import getenv
from flask import Flask
from flask import abort
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth

from settings import ALLOWED_HOSTS
from settings import SERVER_NAME
from settings import API_VERSION
from settings import SQLALCHEMY_TRACK_MODIFICATIONS
from settings import SQLALCHEMY_DATABASE_URI
from settings import RESTFUL_JSON_SETTINGS
from settings import RECAPTCHA_PARAMETERS
from settings import RECAPTCHA_DATA_ATTRS
from settings import RECAPTCHA_SCRIPT
from settings import RECAPTCHA_DIV_CLASS
from settings import RECAPTCHA_VERIFY_SERVER
from settings import OAUTH2_PROVIDER_NAME
from settings import OAUTH2_SERVER_METADATA_URL
from settings import OAUTH2_CLIENT_KEYWORD_ARGUMENTS

from helpers.flask_utility import TomChienXuOJ_redirect as redirect
from helpers.flask_utility import TomChienXuOJ_render_template as render_template
from helpers.time import datetime_to_arrow

from .blueprints import api_blueprint

load_dotenv()

app = Flask(__name__, subdomain_matching=True)

app.config["SECRET_KEY"] = getenv("SECRET_KEY")
app.config["SERVER_NAME"] = SERVER_NAME
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["RESTFUL_JSON"] = RESTFUL_JSON_SETTINGS
app.config["RECAPTCHA_PUBLIC_KEY"] = getenv("RECAPTCHA_PUBLIC_KEY")
app.config["RECAPTCHA_PRIVATE_KEY"] = getenv("RECAPTCHA_PRIVATE_KEY")
app.config["RECAPTCHA_PARAMETERS"] = RECAPTCHA_PARAMETERS
app.config["RECAPTCHA_DATA_ATTRS"] = RECAPTCHA_DATA_ATTRS
app.config["RECAPTCHA_SCRIPT"] = RECAPTCHA_SCRIPT
app.config["RECAPTCHA_DIV_CLASS"] = RECAPTCHA_DIV_CLASS
app.config["RECAPTCHA_VERIFY_SERVER"] = RECAPTCHA_VERIFY_SERVER

database = SQLAlchemy(app)
api = Api(api_blueprint.blueprint, prefix=f"/v{API_VERSION}")
login_manager = LoginManager(app)
oauth = OAuth(app)

google_oauth2 = oauth.register(
  OAUTH2_PROVIDER_NAME,
  client_id=getenv("OAUTH2_CLIENT_ID"),
  client_secret=getenv("OAUTH2_CLIENT_SECRET"),
  server_metadata_url=OAUTH2_SERVER_METADATA_URL,
  client_kwargs=OAUTH2_CLIENT_KEYWORD_ARGUMENTS,
)

@app.before_request
def request_validation():
  host = request.host
  if host not in ALLOWED_HOSTS:
    abort(403, f"This is not a registered Base Domain!\nYou are accessing this website through: {host}")

from . import api_module
from . import page_loader
from . import recaptcha_localization

from models import *
with app.app_context():
  database.create_all()

from arrow import get

login_manager.login_view = "main.homepage"

@login_manager.user_loader
def load_user(user_id):
  with database.session.no_autoflush:
    user = User.query.get(user_id)
    user.arrow_created_at = datetime_to_arrow(user.created_at)
    user.arrow_api_key_created_at = datetime_to_arrow(user.api_key_created_at)

    return user