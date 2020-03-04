import os


class Default(object):
    from dotenv import load_dotenv
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '../../.flaskenv'))
    app_settings = os.environ.get('APP_SETTINGS')
    #DEBUG = True
    # You need to replace the next values with the appropriate values for your configuration
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "Top-Secrate"
    JWT_SECRET_KEY = "JWT-SECRATE"
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_TOKEN_LOCATION = 'headers'
    TRAP_BAD_REQUEST_ERRORS = True
    RESTPLUS_MASK_SWAGGER = True
    CORS_ORIGIN_WHITELIST = [
        'http://0.0.0.0:5000',
        'http://localhost:4100',
        'http://0.0.0.0:8080',
        'http://localhost:8000',
        'http://0.0.0.0:4200',
        'http://localhost:4200',
        'http://0.0.0.0:4000',
        'http://localhost:4000',
        'https://shipskart-2b3bb.web.app'
    ]
    TEMP_DIR = os.path.join(basedir, '../temp_export_files/')

