
import os


class Config(object):
    """
    Base class for applicaiton configuration.
    """
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')

    HERE_APP_ID = os.environ.get("APP_ID")
    if not HERE_APP_ID:
        with open("app_id") as app_id:
            HERE_APP_ID = app_id.read().strip()

    HERE_APP_CODE = os.environ.get("APP_CODE")
    if not HERE_APP_CODE:
        with open("app_code") as app_code:
            HERE_APP_CODE = app_code.read().strip()

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True


config = {
    'dev': DevConfig,
    'default': Config
}
