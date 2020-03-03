from marshmallow import ValidationError

from api.helpers.jwt_helper import JWT
from api.modules.user_token import UserToken
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


def make_admin(user_id: int):
    user: UserModel = UserModel.get_by_id(user_id)
    from api.helpers.response import ApiResponse
    if user is not None:
        from api.common.enums import RoleType
        user.role.role_type = RoleType.SUPER_ADMIN.value
        user.update()

        tokens = UserToken.query.filter_by(user_id=user_id).all()
        for token in tokens:
            token.delete()

    return ApiResponse.error('User not found.', 402)


update_parser = UserModel.get_parser_user_profile_update()
