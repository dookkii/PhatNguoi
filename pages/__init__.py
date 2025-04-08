from os import getenv
from flask import Flask
from flask import abort
from flask import request
from flask_restful import Api
from dotenv import load_dotenv

from settings import ALLOWED_HOST
from settings import SERVER_NAME
from settings import API_VERSION
from settings import RESTFUL_JSON_SETTINGS

from helpers.flask_utility import TomChienXuOJ_redirect as redirect
from helpers.flask_utility import TomChienXuOJ_render_template as render_template

from .blueprints import api_blueprint

load_dotenv()

app = Flask(__name__, subdomain_matching=True)
api = Api(api_blueprint.blueprint, prefix=f"/v{API_VERSION}")

app.config["SECRET_KEY"] = getenv("SECRET_KEY")
app.config["SERVER_NAME"] = SERVER_NAME
app.config["RESTFUL_JSON"] = RESTFUL_JSON_SETTINGS

@app.before_request
def request_validation():
  host = request.host
  if host not in ALLOWED_HOST:
    abort(403, f"This is not a registered Base Domain!\nYou are accessing this website through: {host}")

from . import api_module
from . import page_loader