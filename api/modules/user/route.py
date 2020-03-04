from api.modules.user.resource import ns_user, UserProfile, Registration, Login, Logout, UpdatePassword, User

ns_user.add_resource(User, '/listing')
ns_user.add_resource(UserProfile, '/')
ns_user.add_resource(Registration, '/registration')
ns_user.add_resource(Login, '/login')
ns_user.add_resource(Logout, '/logout')
ns_user.add_resource(UpdatePassword, '/updatepassword')
