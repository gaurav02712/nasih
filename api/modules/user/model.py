import re

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_restplus import reqparse
from marshmallow import ValidationError
from sqlalchemy.orm import validates
from werkzeug.datastructures import FileStorage

from api.common.base.model import BaseModel
from api.config.initialization import db


class UserModel(BaseModel):
    __tablename__ = 'user'
    f_name = db.Column(db.String(45), nullable=False)
    l_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=True, unique=False)
    username = db.Column(db.String(45), nullable=True, unique=True)
    date_of_birth = db.Column(db.Date)
    email_verified = db.Column(db.Boolean, nullable=False, default=False)
    social_id = db.Column(db.String(50), nullable=True)
    register_by = db.Column(db.String(50), nullable=True, default='Nasih')
    device = db.relationship('DeviceInfoModel', cascade="all,delete")
    role = db.relationship('UserRole', uselist=False, cascade="all,delete", lazy=True)
    profile_image_url = db.Column(db.String(255))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = kwargs.get('username', self.email)

    @validates('email')
    def validate_email(self, key, email):
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError('Not a valid email id.')
        else:
            return email

    @property
    def password(self):
        # raise AttributeError('password: write-only field')
        return self.password_hash

    @password.setter
    def password(self, password):
        min_length = 5
        if len(password) < min_length:
            raise ValidationError(f'Password length must be greater than {min_length}.')
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_parser_user_registration(cls):
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('f_name', required=True, type=str)
        parser.add_argument('l_name', required=True, type=str)
        parser.add_argument('email', required=True, type=str)
        parser.add_argument('date_of_birth', required=True, type=str, help='Date Of Birth (YYYY-MM-DD)')
        parser.add_argument('password', required=True)
        return parser

    @classmethod
    def get_parser_user_registration_social(cls):
        parser = UserModel.get_parser_user_registration()
        parser.remove_argument('password')
        parser.add_argument('social_id', required=True, type=str)
        options = ['nasih', 'google', 'facebook']
        parser.add_argument('register_by', required=True, choices=options, type=str, help='facebook/google')
        parser.replace_argument('date_of_birth', required=False, type=str, help='Date Of Birth (YYYY-MM-DD)')
        return parser

    @classmethod
    def get_parser_user_login_social(cls):
        parser = UserModel.get_parser_user_registration_social()
        options = ['nasih', 'google', 'facebook']
        parser.replace_argument('register_by', required=True, choices=options, type=str, help='facebook/google')
        parser.replace_argument('f_name', required=False, type=str)
        parser.replace_argument('l_name', required=False, type=str)
        parser.replace_argument('email', required=False, type=str)
        return parser

    @classmethod
    def get_parser_user_login(cls):
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('email', required=True, type=str)
        parser.add_argument('password', required=True, type=str)
        return parser

    @classmethod
    def get_parser_user_profile_update(cls):
        parser = UserModel.get_parser_user_registration()
        parser.add_argument('profile_image', location='files', type=FileStorage)
        parser.remove_argument('password')
        parser.remove_argument('email')
        return parser

    @classmethod
    def get_parser_update_password(cls):
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('current_password', required=True, type=str)
        parser.add_argument('new_password', required=True, type=str)
        return parser

    @classmethod
    def get_parser_forget_password(cls):
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('email', required=True, type=str, location='form')
        return parser

    @classmethod
    def get_parser_reset_password(cls):
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('token', required=True, type=str, location='form')
        parser.add_argument('new_password', required=True, type=str, location='form')
        return parser


class DeviceInfoModel(BaseModel):
    __tablename__ = 'device_info'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50))
    device_id = db.Column(db.String(255))
    os_type = db.Column(db.String(10))
    os_version = db.Column(db.String(10))
    app_version = db.Column(db.String(10))
    build_version = db.Column(db.String(10))
    model_name = db.Column(db.String(255))
    model_number = db.Column(db.String(255))
    fcm_token = db.Column(db.String(512))
