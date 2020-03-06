from api.modules.user.resource import ns_user, UserProfile, Registration, Login, Logout, UpdatePassword, User, LoginSocial

ns_user.add_resource(User, '/listing')
ns_user.add_resource(UserProfile, '/')
ns_user.add_resource(Registration, '/registration')
ns_user.add_resource(Login, '/login')
ns_user.add_resource(Logout, '/logout')
ns_user.add_resource(UpdatePassword, '/updatepassword')
ns_user.add_resource(LoginSocial, '/login_social')

