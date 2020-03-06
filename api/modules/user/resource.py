from flask import request, g
from flask_bcrypt import generate_password_hash

from api.common import KMessages
from api.common.base.parsers import base_pagination_parser
from api.common.enums import RoleType
from api.config.initialization import api
from api.helpers.aws import AWSManager
from api.helpers.decorators import allow
from api.helpers.extension import Resource
from api.helpers.jwt_helper import jwt_required, JWT
from api.helpers.pagination import get_paginated_list
from api.helpers.response import ApiResponse
from api.modules.user.business import perform_login, perform_logout, password_validation, register_social_media
from api.modules.user.model import UserModel
from api.modules.user.role.model import UserRole
from api.modules.user.schema import UserSchema

ns_user = api.namespace('user', description='User Profile Module')


# @app.route('/')
# @app.route('/index')
# def index():
#     return "Hello, World!"


class User(Resource):
    parser = base_pagination_parser.copy()

    @ns_user.doc(security="Authorization")
    @jwt_required
    @ns_user.expect(parser)
    @allow([RoleType.SUPER_ADMIN])
    def get(self):
        """Get user listing"""
        args = self.parser.parse_args()
        page = args.page
        per_page = args.limit
        user_paginatior = UserModel.query.paginate(page=page, per_page=per_page)
        return ApiResponse.success(get_paginated_list(user_paginatior, UserSchema(many=True), per_page), 200)


class UserProfile(Resource):

    @ns_user.doc(params={'user_id': 'optional user id (Int value), if we need to find other user details '})
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
        profile_image = json_data['profile_image']
        if profile_image:
            json_data['profile_image_url'] = AWSManager().updateImage(json_data['profile_image'])
        user: UserModel = UserModel.get_by_id(g.user_id)
        user.update(**json_data)
        return ApiResponse.success(UserSchema().dump(user), 200)


class Registration(Resource):
    parser = UserModel.get_parser_user_registration()

    @ns_user.expect(parser)
    def post(self):
        """Registration via Email"""
        user: UserModel = self.validObject(self.parser, UserSchema())
        user.password = user.create_password()
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
        user = register_social_media(json)
        if user:
            loggeding_data = perform_login(user)
            return ApiResponse.success(loggeding_data, 200, message=KMessages.LOGIN_DONE)
        userquery = UserModel.query.filter(UserModel.email == json['email'], UserModel.is_deleted == False)
        user = userquery.first()
        if user is not None:
            authorized = user.check_password(json['password'])
            if authorized:
                loggeding_data = perform_login(user)
                return ApiResponse.success(loggeding_data, 200, message=KMessages.LOGIN_DONE)
            else:
                return ApiResponse.error(None, 404, message=KMessages.INVALID_LOGIN_AUTH)
        else:
            return ApiResponse.error(None, 404, message=KMessages.NO_EMAIL_ID)


class LoginSocial(Resource):
    parser = UserModel.get_parser_user_registration_social()

    @ns_user.expect(parser)
    def post(self):
        """Login/registration via Social Account"""
        json = self.parser.parse_args()
        newuser = self.validObject(self.parser, UserSchema())
        user = register_social_media(json, newuser)
        if user:
            loggeding_data = perform_login(user)
            return ApiResponse.success(loggeding_data, 200, message=KMessages.LOGIN_DONE)
        return ApiResponse.error(None, 404, message=KMessages.INVALID_LOGIN_AUTH)


class Logout(Resource):
    @ns_user.doc(security="Authorization")
    @jwt_required
    def post(self):
        """Perform logout"""
        user_token = JWT.get_auth_token()
        perform_logout(user_token.token)
        return ApiResponse.success(None, 200, message=KMessages.LOGOUT_DONE)


class UpdatePassword(Resource):
    parser = UserModel.get_parser_update_password()

    @ns_user.doc(security="Authorization")
    @jwt_required
    @ns_user.expect(parser)
    def post(self):
        """Update userpasword"""
        arg_json = self.parser.parse_args()
        user: UserModel = UserModel.get_by_id(g.user_id)
        authorized = user.check_password(arg_json['current_password'])
        if not authorized:
            return ApiResponse.error(None, 404, message=KMessages.CURRENT_PASSWORD_DIFFER)
        new_password = arg_json['new_password']
        password_validation(new_password)
        user.password = generate_password_hash(new_password).decode('utf8')
        user.update()
        return ApiResponse.success(None, 200, message=KMessages.PASSWORD_CHANGE_SUCESSFULLY)
