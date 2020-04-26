import os
from datetime import timedelta
from api.config.default import Default


class DevConfig(Default):
    """Development configuration."""
    DEBUG = True
    DB_URL = os.environ.get('DB_URL')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(10 ** 6)
