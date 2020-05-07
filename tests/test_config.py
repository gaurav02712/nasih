# tests/test_config.py
import unittest

from app import create_app


class TestTestingConfig(unittest.TestCase):

    def setUp(self):
        self.app = create_app('api.config.testing.TestingConfig')

    def test_app_is_testing(self):
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertTrue(self.app.config['TESTING'])


class TestDevelopmentConfig(unittest.TestCase):

    def setUp(self):
        self.app = create_app('api.config.development.DevelopmentConfig')

    def test_app_is_development(self):
        self.assertTrue(self.app.config['DEBUG'] is True)


class TestStagingConfig(unittest.TestCase):

    def setUp(self):
        self.app = create_app('api.config.staging.StagingConfig')

    def test_app_is_staging(self):
        self.assertTrue(self.app.config['DEBUG'] is False)


class TestProductionConfig(unittest.TestCase):

    def setUp(self):
        self.app = create_app('api.config.production.ProductionConfig')

    def test_app_is_staging(self):
        self.assertTrue(self.app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
