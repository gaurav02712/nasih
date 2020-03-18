from marshmallow import ValidationError

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
