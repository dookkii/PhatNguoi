from . import app

from settings import SUBDOMAIN_API
from settings import SUBDOMAIN_MAIN_PAGE

from .blueprints import api_blueprint
from .blueprints import main_blueprint

app.register_blueprint(api_blueprint.blueprint, subdomain=SUBDOMAIN_API)
app.register_blueprint(main_blueprint.blueprint, subdomain=SUBDOMAIN_MAIN_PAGE)