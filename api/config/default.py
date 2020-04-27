import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../../.flaskenv'))
app_settings = os.environ.get('APP_SETTINGS')


class Default(object):
    DEBUG = True
    SERVER_NAME = os.environ.get('SERVER_NAME')
    # You need to replace the next values with the appropriate values for your configuration
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    DATABASE_HOST = os.environ.get('DATABASE_HOST')
    DATABASE_NAME = os.environ.get('DATABASE_NAME')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(
        DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME
    ) or 'sqlite:///' + os.path.join(basedir, 'app.db')

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kiss-my-shiny-metal-ass'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or 'kiss-my-shiny-metal-ass'
    JWT_SECRET_KEY = "JWT-SECRET"
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
    QUESTION_ICONS_DIR = os.path.join(TEMP_DIR, 'questions_icons/')
    USER_DP_DIR = os.path.join(TEMP_DIR, 'profile_pic/')

    # Mail Config
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
