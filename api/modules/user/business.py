import os
from time import time
from marshmallow import ValidationError
import jwt

from api.helpers.jwt_helper import JWT
from api.modules.user.model import UserModel
from api.modules.user.schema import UserSchema


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


def get_reset_password_token(user: UserModel, expires_in=600):
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    data_dict = {'reset_password': user.id, 'exp': time() + expires_in}
    # return create_access_token(identity={JWT_SECRET_KEY: data_dict}, expires_delta=expires_in)
    token = jwt.encode(data_dict, JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')
    decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
    return token


# access_token = create_access_token(identity=user, expires_delta=expires)


def verify_reset_password_token(token) -> UserModel:
    try:
        JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
        user_id = jwt.decode(token, JWT_SECRET_KEY,
                             algorithms=['HS256'])['reset_password']
    except Exception as e:
        raise e
    return UserModel.get_by_id(user_id)
