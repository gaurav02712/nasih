from api.common.enums import RoleType
from api.config.initialization import db


class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    role_type = db.Column(db.String)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), unique=True)


    # def __init__(self, role_type: str, user_id: int):
    #     if RoleType.has_value(role_type):
    #         self.role_type = role_type
    #         self.user_id = user_id

    def __init__(self, role: RoleType, user_id: int):
        self.role_type = role.value
        self.user_id = user_id

    def __init__(self, role: RoleType):
        self.role_type = role.value
