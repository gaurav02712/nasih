from api.modules.user.resource import ns_user, UserProfile, Registration, Login, Logout

ns_user.add_resource(UserProfile, '/')
ns_user.add_resource(Registration, '/registration')
ns_user.add_resource(Login, '/login')
ns_user.add_resource(Logout, '/logout')




