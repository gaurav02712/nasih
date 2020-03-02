from datetime import timedelta
from functools import wraps
from flask import request, abort, g
from flask_jwt_extended import (create_access_token, create_refresh_token, verify_jwt_in_request, get_jwt_claims,
                                get_raw_jwt)

from api.modules.user_token import UserToken
from api.helpers.response import ApiResponse


def jwt_required(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        verify_jwt_in_request()
        authorization = request.headers.get('Authorization')
        if not authorization:
            return ApiResponse.error('No authorization token provided', 403)
        auth_token = authorization.split(" ")[1]
        resp = UserToken.is_token_valid(auth_token)
        if not resp:
            return ApiResponse.error('Invalid authorization token', 403)
        # validate = JWT.validate_authorization(auth_token)
        #
        from flask_jwt_extended import get_jwt_identity
        user = get_jwt_identity()
        # clam = get_jwt_claims()
        g.user_id = user['user_id']
        #
        # from api.modules.user.role.model import UserRole
        # g.user_role: UserRole = UserRole.query.filter_by(user_id=g.user_id).first()
        #
        # if not validate:
        #     return ApiResponse.error('Unauthorized', 403)
        return fn(self, *args, **kwargs)

    return wrapper


class JWT:
    def validate_authorization(self, token: str):
        token_user = UserToken.query.filter_by(token=self).first()
        roles = get_jwt_claims()
        if roles is None:
            return False
        else:
            return True

    # Here is a custom decorator that verifies the JWT is present in
    # the request, as well as insuring that this user has a role of
    # `admin` in the access token

    @classmethod
    def create_tokens(cls, user):
        expires = timedelta(days=30)
        access_token = create_access_token(identity=user, expires_delta=expires)
        refresh_token = create_refresh_token(identity=user, expires_delta=False)
        UserToken(token=access_token, refresh_token=refresh_token, user_id=user.id).save()
        auth_token = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return auth_token

    @classmethod
    def expire_token(cls, token):
        jti = get_raw_jwt()['jti']
        # blacklist.add(jti)

    @classmethod
    def get_user_by_token(cls):
        try:
            # token = JWT.get_user_by_token()
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[1]
            token = UserToken.query.filter_by(token=auth_token).first()
            return auth_token.user_id
        except:
            return None

    @classmethod
    def get_auth_token(cls):
        try:
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[1]
            token = UserToken.query.filter_by(token=auth_token).first()
            return token
        except:
            abort(400, 'Invlaid authorization token ')
