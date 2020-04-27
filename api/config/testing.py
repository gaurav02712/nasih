import os
from api.config import Default


class TestingConfig(Default):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(os.environ.get('DATABASE_USER'),
                                                                os.environ.get('DATABASE_PASSWORD'),
                                                                os.environ.get('DATABASE_HOST'),
                                                                'test_db')
    DEBUG = True
