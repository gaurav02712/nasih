# tests/test_config.py
import unittest

from flask import current_app

from app import app


class TestTestingConfig(unittest.TestCase):

    def setUp(self):
        app.config.from_object('api.config.testing.TestingConfig')

        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertTrue(current_app.config['TESTING'])


class TestDevelopmentConfig(unittest.TestCase):

    def setUp(self):
        app.config.from_object('api.config.development.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['DEBUG'] is True)


class TestStagingConfig(unittest.TestCase):

    def setUp(self):
        app.config.from_object('api.config.staging.TestStagingConfig')
        return app

    def test_app_is_staging(self):
        self.assertTrue(app.config['DEBUG'] is False)


class TestProductionConfig(unittest.TestCase):

    def setUp(self):
        app.config.from_object('api.config.production.ProductionConfig')
        return app

    def test_app_is_staging(self):
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
