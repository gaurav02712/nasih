import os
from flask import Flask

from api.config.default import app_settings
from api.config.initialization import blueprint, prepare_libraries, register_header
from api.helpers import errorhandler


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    prepare_libraries(app)
    app.register_blueprint(blueprint)
    errorhandler.register_error_handlers(app)
    register_header(app)
    return app


def _check_config_variables_are_set(config):

    assert config['SERVER_NAME'] is not None, \
        'SERVER_NAME is not set, set the env variable SERVER_NAME ' \
        'or SERVER_NAME in the production config file.'

    assert config['DATABASE_HOST'] is not None, \
        'DATABASE_HOST is not set, set the env variable DATABASE_HOST ' \
        'or DATABASE_HOST in the production config file.'

    assert config['DATABASE_USER'] is not None, \
        'DATABASE_USER is not set, set the env variable DATABASE_USER ' \
        'or DATABASE_USER in the production config file.'

    assert config['DATABASE_NAME'] is not None, \
        'DATABASE_NAME is not set, set the env variable DATABASE_NAME ' \
        'or DATABASE_NAME in the production config file.'

    if os.environ['APP_SETTINGS'] == 'project.config.production.ProductionConfig':
        assert config['FCM_API_KEY'] is not None,\
            'FCM_API_KEY is not set, set it in the production config file.'
        assert config['FCM_API_KEY'] is not None,\
            'FCM_API_KEY is not set, set it in the production config file.'


app = create_app(app_settings)
app.app_context().push()
_check_config_variables_are_set(app.config)
