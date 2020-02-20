from marshmallow import fields, ValidationError, validates
from api.config.initialization import ma
from api.modules.user.model import UserModel


class UserSchema(ma.ModelSchema):
    date_of_birth = fields.Date('%Y-%m-%d')
    password = fields.String(load_only=True)

    @validates("password")
    def validate_password(self, password):
        from api.modules.user.business import password_validation
        password_validation(password)

    class Meta:
        model = UserModel
        include_fk = True
        exclude = model.baseExcluded()
