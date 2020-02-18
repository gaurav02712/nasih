
from datetime import timedelta
from flask import current_app
from api.config.default import Default


class StagingConfig(Default):
    """Development configuration."""
    DEBUG = True
    DB_URL = 'postgresql://Gaurav:@localhost:5433/nasih'
    SQLALCHEMY_DATABASE_URI = DB_URL
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(10 ** 6)
    # CACHE_TYPE = 'redis'
    # REDIS_URL = "redis://localhost:6379/0"


