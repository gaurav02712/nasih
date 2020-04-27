import os
from api.config import Default


class TestingConfig(Default):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    TEST_USER_EMAIL = os.environ.get('TEST_USER_EMAIL')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(os.environ.get('DATABASE_USER'),
                                                                os.environ.get('DATABASE_PASSWORD'),
                                                                os.environ.get('DATABASE_HOST'),
                                                                'test_db')
    DEBUG = True
