import re
from flask_bcrypt import generate_password_hash, check_password_hash
from marshmallow import ValidationError
from werkzeug.datastructures import FileStorage
from api.common.base.model import BaseModel
from api.config.initialization import db
from flask_restplus import reqparse
from sqlalchemy.orm import validates

from api.modules.user.role.model import UserRole


class UserModel(BaseModel):
    __tablename__ = 'user'
    f_name = db.Column(db.String(45), nullable=False)
    l_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(355), nullable=False, unique=False)
    username = db.Column(db.String(45), nullable=True, unique=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    is_varified = db.Column(db.Integer, nullable=False, default=0)
    varified_by = db.Column(db.Integer, nullable=False, default=0)
    device = db.relationship('DeviceInfoModel', cascade="all,delete")
    role = db.relationship('UserRole', uselist=False, cascade="all,delete", lazy=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = kwargs.get('username', self.email)
        self.password = generate_password_hash(self.password).decode('utf8')

    @validates('email')
    def validate_email(self, key, email):
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError('Not a valid email id.')
        elif UserModel.query.filter(UserModel.email == email).first():
            raise ValidationError('Email id is alredy registered.')
        else:
            return email

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_parser_user_registration(cls):
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('f_name', required=True, type=str)
        parser.add_argument('l_name', required=True, type=str)
        parser.add_argument('email', required=True, type=str)
        parser.add_argument('date_of_birth', required=False, type=str, help='Date Of Birth (YYYY-MM-DD)')
        parser.add_argument('password', required=True)
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
        parser.add_argument('display_image', location='files', type=FileStorage)
        parser.remove_argument('password')
        parser.remove_argument('email')
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
