from functools import wraps
from flask_jwt_extended import get_jwt_claims

from api.helpers.response import ApiResponse


def allow(roleTypes: list = None):
    def allow_access(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            response = False
            if roleTypes is not None:
                for roleType in roleTypes:
                    user_role_type = get_jwt_claims()['user_role']
                    if user_role_type == roleType.value:
                        response = True

            if response is False:
                return ApiResponse.error(f'user is is not authorized to perform this access', 403)
            return fn(*args, **kwargs)
        return wrapper
    return allow_access
