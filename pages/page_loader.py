from . import app

from settings import SUBDOMAIN_API
from settings import SUBDOMAIN_MAIN_PAGE

from .blueprints import api_blueprint
from .blueprints import main_blueprint
from .blueprints import profile_blueprint
from .blueprints import authentication_blueprint

app.register_blueprint(api_blueprint.blueprint, subdomain=SUBDOMAIN_API)
app.register_blueprint(main_blueprint.blueprint, subdomain=SUBDOMAIN_MAIN_PAGE)
app.register_blueprint(authentication_blueprint.blueprint)
app.register_blueprint(profile_blueprint.blueprint, url_prefix="/profile")