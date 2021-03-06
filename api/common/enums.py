from api.common.base.enum import BaseEnum


class RoleType(BaseEnum):
    SUPER_ADMIN = 'SUPER_ADMIN'  # An SUPER admin
    USER = 'USER'  # a normal user


class BookingStatus(BaseEnum):
    CONFIRM = 1
    CANCELLED = 2
