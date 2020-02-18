from flask import request, g
from flask_jwt_extended import get_jwt_identity

from api.common import KMessages
from api.common.enums import RoleType
from api.config.initialization import api
from api.helpers.extension import Resource
from api.helpers.jwt_helper import jwt_required, JWT
from api.helpers.response import ApiResponse
from api.modules.user.business import perform_login, perform_logout
from api.modules.user.model import UserModel
from api.modules.user.role.model import UserRole
from api.modules.user.schema import UserSchema

ns_user = api.namespace('user', description='User Profile Module')


# @app.route('/')
# @app.route('/index')
# def index():
#     return "Hello, World!"

class UserProfile(Resource):
    @ns_user.doc(params={'user_id': 'an Int value'})
    @ns_user.doc(security="Authorization")
    @jwt_required
    def get(self):
        """Get User data"""
        user_id = request.args.get('user_id', None, type=int)
        if user_id is None:
            user_id = g.user_id
        user = UserModel.get_by_id(user_id)
        if user is not None:
            return ApiResponse.success(UserSchema().dump(user), 200)
        return ApiResponse.error('User not found.', 402)

    update_parser = UserModel.get_parser_user_profile_update()

    @ns_user.doc(security="Authorization")
    @jwt_required
    @ns_user.expect(update_parser)
    def put(self):
        """Update user profile data"""
        from api.modules.user.model import UserModel
        json_data = self.update_parser.parse_args()
        json_data['profileImage'] = None
        user: UserModel = UserModel.get_by_id(g.user_id)
        user.update(**json_data)
        return ApiResponse.success(UserSchema().dump(user), 200)


class Registration(Resource):
    parser = UserModel.get_parser_user_registration()

    @ns_user.expect(parser)
    def post(self):
        """Registration via Email"""
        user: UserModel = self.validObject(self.parser, UserSchema())
        user.role = UserRole(RoleType.USER)
        user.save()
        loggeding_data = perform_login(user)
        return ApiResponse.success(loggeding_data, 200, message=KMessages.REGISTRATION_DONE)


class Login(Resource):
    parser = UserModel.get_parser_user_login()

    @ns_user.expect(parser)
    def post(self):
        """Login via Email"""
        json = self.parser.parse_args()
        user: UserModel = UserModel.query.filter(UserModel.email == json['email']).first()
        if user is not None:
            authorized = user.check_password(json['password'])
            if authorized:
                loggeding_data = perform_login(user)
                return ApiResponse.success(loggeding_data, 200, message=KMessages.LOGIN_DONE)
            else:
                return ApiResponse.error(None, 404, message=KMessages.INVALID_LOGIN_AUTH)
        else:
            return ApiResponse.error(None, 404, message=KMessages.NO_EMAIL_ID)


class Logout(Resource):
    @ns_user.doc(security="Authorization")
    @jwt_required
    def post(self):
        """Perform logout"""
        user_token = JWT.get_auth_token()
        perform_logout(user_token.token)
        return ApiResponse.success(None, 200, message=KMessages.LOGOUT_DONE)
