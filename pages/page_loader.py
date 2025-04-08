from . import app

from .blueprints import api_blueprint
from .blueprints import main_blueprint

app.register_blueprint(api_blueprint.blueprint, subdomain="api")
app.register_blueprint(main_blueprint.blueprint, subdomain=None)