from flask import request, g
from flask_bcrypt import generate_password_hash

from api.common import KMessages
from api.common.enums import RoleType
from api.config.initialization import api
from api.helpers.aws import AWSManager
from api.helpers.extension import Resource
from api.helpers.jwt_helper import jwt_required, JWT
from api.helpers.response import ApiResponse
from api.modules.user.business import perform_login, perform_logout, password_validation, register_social_media, \
    verify_reset_password_token, generate_confirmation_token, confirm_token
from api.modules.user.model import UserModel
from api.modules.user.notification.model import NotificaionModel
from api.modules.user.notification.schema import NotificaionModelSchema
from api.modules.user.role.model import UserRole
from api.modules.user.schema import UserSchema
from api.helpers.email import send_password_reset_confirmation_email, send_password_reset_request_email

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
        profile_image = json_data['profile_image']
        if profile_image:
            from flask import current_app
            directory_path = current_app.config['USER_DP_DIR']
            json_data['profile_image_url'] = AWSManager().updateImage(profile_image, directory_path)
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
        logged_in_data = perform_login(user)
        return ApiResponse.success(logged_in_data, 201, message=KMessages.REGISTRATION_DONE)


class Login(Resource):
    parser = UserModel.get_parser_user_login()

    @ns_user.expect(parser)
    def post(self):
        """Login via Email"""
        json = self.parser.parse_args()
        user = UserModel.query.filter(UserModel.email == json['email'], UserModel.is_deleted == False).first()
        if user:
            authorized = user.check_password(json['password'])
            if authorized:
                logged_in_data = perform_login(user)
                return ApiResponse.success(logged_in_data, 200, message=KMessages.LOGIN_DONE)
            else:
                return ApiResponse.error(None, 404, message=KMessages.INVALID_LOGIN_AUTH)
        else:
            return ApiResponse.error(None, 404, message=KMessages.NO_EMAIL_ID)


class LoginSocial(Resource):
    login_parser = UserModel.get_parser_user_login_social()

    @ns_user.expect(login_parser)
    def post(self):
        """Login via Social id/Registration via social id & detail"""
        json = self.login_parser.parse_args()
        social_id = json['social_id']

        user = UserModel.query.filter(UserModel.social_id == social_id, UserModel.is_deleted == False).first()
        message = KMessages.LOGIN_DONE
        if user is None:
            parser_registration = UserModel.get_parser_user_registration_social()
            new_user: UserModel = self.validObject(parser_registration, UserSchema())
            new_user.role = UserRole(RoleType.USER)
            new_user.save()
            user = new_user
            message = KMessages.REGISTRATION_DONE
        logged_in_data = perform_login(user)
        return ApiResponse.success(logged_in_data, 200, message=message)


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
        """Update user's password"""
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


class ForgotPasswordToken(Resource):
    parser = UserModel.get_parser_forget_password()

    @ns_user.expect(parser)
    def post(self):
        """Get Token for Forget password"""
        arg_json = self.parser.parse_args()
        email = arg_json['email']
        user: UserModel = UserModel.query.filter(UserModel.email == email).first()

        if not user:
            return ApiResponse.error(None, 404, message=KMessages.NO_EMAIL_ID)

        send_password_reset_request_email(user)
        return ApiResponse.success(None, 200, message=KMessages.RESET_PASSWORD_TOKEN_SEND)


class ResetPassword(Resource):
    parser = UserModel.get_parser_reset_password()

    @ns_user.expect(parser)
    def post(self):
        """Reset your password with token"""
        arg_json = self.parser.parse_args()
        # user: UserModel = verify_reset_password_token(arg_json.token)
        email = confirm_token(token=arg_json.token)

        if not email:
            return ApiResponse.error(None, 404, message=KMessages.INVALID_TOKEN)

        user = UserModel.query.filter_by(email=email).first()
        user.password = arg_json.new_password
        user.update()
        send_password_reset_confirmation_email(user)
        return ApiResponse.success(None, 200, message=KMessages.PASSWORD_CHANGE_SUCESSFULLY)


class UserNotification(Resource):
    parser = NotificaionModel.get_parser_fetch_notification()

    @ns_user.expect(parser)
    @ns_user.doc(security="Authorization")
    @jwt_required
    def get(self):
        """Fetch user notification"""
        args = self.parser.parse_args()
        page = args.page
        per_page = args.limit
        records = NotificaionModel.query.filter(NotificaionModel.user_id == g.user_id).paginate(page, per_page, False)
        from api.helpers.pagination import get_paginated_list
        return ApiResponse.success(get_paginated_list(records, NotificaionModelSchema(many=True), per_page), 200)
