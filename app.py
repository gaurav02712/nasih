import os
from flask import Flask
from api.config.development import DevConfig
from api.config.staging import StagingConfig
from api.helpers import errorhandler

app = Flask(__name__)


def create_app(config_obj):
    from api.config.initialization import blueprint, prepare_libraries, register_header
    app.config.from_object(config_obj)
    prepare_libraries(app)
    app.register_blueprint(blueprint)
    errorhandler.register_error_handlers(app)
    register_header(app)
    # clear_session_with_rollback()
    return app


env = os.environ.get('FLASK_ENV')
en = os.environ
config = StagingConfig if env == 'staging' else DevConfig
app = create_app(DevConfig)
app.app_context().push()
