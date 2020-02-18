from api.config.initialization import ma
from api.modules.user.role.model import UserRole


class UserRoleSchema(ma.ModelSchema):
    class Meta:
        model = UserRole
