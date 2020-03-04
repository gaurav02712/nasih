def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']


def add_claims_to_access_token(user):
    return {'user_role': user.role.role_type}


def user_identity_lookup(user):
    return {'email': user.username, 'user_id': user.id, }
