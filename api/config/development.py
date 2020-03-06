import os
from datetime import timedelta
from api.config.default import Default


class DevConfig(Default):
    """Development configuration."""
    DEBUG = True
    # DB_URL = os.environ.get('DB_URL')
    DB_URL = 'postgresql://Gaurav:@localhost:5433/nasih'
    # Put the db file in project root
    SQLALCHEMY_DATABASE_URI = DB_URL
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(10 ** 6)
    # CACHE_TYPE = 'redis'  # Can be "memcached", "redis", etc.
    # REDIS_URL = "redis://localhost:6379/0"
