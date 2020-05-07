import os
from time import time
import jwt
from itsdangerous import URLSafeTimedSerializer
from marshmallow import ValidationError

from api.helpers.jwt_helper import JWT
from api.modules.user.model import UserModel
from api.modules.user.schema import UserSchema
from flask import current_app


def perform_login(user: UserModel) -> dict:
    auth_token_dict = JWT.create_tokens(user)
    userjson = UserSchema().dump(user)
    # data = userjson.data
    return {'auth': auth_token_dict, 'user': userjson}


def perform_logout(token: str):
    # TODO:- need to disbale toen form jwt server also
    from api.modules import UserToken
    UserToken.delete_token(token)


def password_validation(password: str):
    min_lenght = 5
    if len(password) < min_lenght:
        raise ValidationError(f'Password length must be greater than {min_lenght}.')


def register_socially(json, newuser):
    from api.modules.user.role.model import UserRole
    from api.common.enums import RoleType
    user = UserModel.query.filter(UserModel.social_id == json['social_id'], UserModel.is_deleted == False).first()
    if user is None:
        new_user = self.validObject(self.parser, UserSchema())

        user = UserModel.query.filter(UserModel.email == json['email'], UserModel.is_deleted == False).first()
        if user:
            user.social_id = json['social_id']
            user.register_by = user.register_by if user.register_by else json['register_by']
            user.f_name = user.f_name if user.f_name else json['f_name']
            user.l_name = user.l_name if user.l_name else json['l_name']
            user.updtae()
        else:
            user = newuser
            user.role = UserRole(RoleType.USER)
            user.save()
        return user
    else:
        return user


def register_social_media(json, newuser):
    from api.modules.user.role.model import UserRole
    from api.common.enums import RoleType
    if json['social_id']:
        user = UserModel.query.filter(UserModel.social_id == json['social_id'], UserModel.is_deleted == False).first()
        if user is None and json['email']:
            user = UserModel.query.filter(UserModel.email == json['email'], UserModel.is_deleted == False).first()
            if user:
                user.social_id = json['social_id']
                user.register_by = user.register_by if user.register_by else json['register_by']
                user.f_name = user.f_name if user.f_name else json['f_name']
                user.l_name = user.l_name if user.l_name else json['l_name']
                user.updtae()
            else:
                user = newuser
                user.role = UserRole(RoleType.USER)
                user.save()
            return user
        else:
            return user
    return False


def get_reset_password_token(user: UserModel, expires_in=600):
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    data_dict = {'reset_password': user.id, 'exp': time() + expires_in}
    # return create_access_token(identity={JWT_SECRET_KEY: data_dict}, expires_delta=expires_in)
    token = jwt.encode(data_dict, JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')
    decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
    return token


def verify_reset_password_token(token) -> UserModel:
    try:
        JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
        user_id = jwt.decode(token, JWT_SECRET_KEY,
                             algorithms=['HS256'])['reset_password']
    except Exception as e:
        raise e
    return UserModel.get_by_id(user_id)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        result = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return result
