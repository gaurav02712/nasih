import unittest

from api.config.initialization import db
from api.modules.user.business import generate_confirmation_token
from api.modules.user.model import UserModel
from app import create_app


def create_user(self):
    self.count += 1
    user = UserModel()
    user.f_name = 'Rocky'
    user.l_name = 'Balboa'
    user.email = 'test+{}@test.com'.format(self.count)
    user.save()
    return user


class TestUser(unittest.TestCase):
    def setUp(self):
        self.app = create_app('api.config.testing.TestingConfig')
        self.client = self.app.test_client
        self.count = 0

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def test_user_registration(self):
        with self.app.app_context():
            response = self.client().post('/v1/user/registration', data=dict(
                f_name='Rambo',
                l_name='Singh',
                email='rambo@singh.com',
                date_of_birth='2020-09-01',
                password='mokonapatobhaiya'
            ))
            self.assertTrue(response.status_code == 201)

    def test_forgot_password(self):
        with self.app.app_context():
            user = create_user(self)
            response = self.client().post('/v1/user/forgot_password', data=dict(
                email=user.email,
            ))
            self.assertTrue(response.status_code == 200)

    def test_reset_forgotten_password_valid_token(self):
        with self.app.app_context():
            user = create_user(self)
            token = generate_confirmation_token(email=user.email)
            response = self.client().post('/v1/user/reset_password', data=dict(
                token=token,
                new_password='papukopatachalgaya'
            ))

            self.assertTrue(response.status_code == 200)

            data = response.get_json()

            self.assertEqual(data['status'], True)


if __name__ == '__main__':
    unittest.main()
