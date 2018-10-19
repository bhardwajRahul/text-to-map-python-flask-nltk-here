
from config import config

from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    if not config_name in config:
        raise ValueError("Invalid FLASK_CONFIG, choose one of %s" %
                str.join(',', config.keys()))
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/1.0')

    return app
