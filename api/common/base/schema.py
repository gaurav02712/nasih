from marshmallow import EXCLUDE, fields, post_dump

from apis.configs.initialization import ma
from apis.helpers.utils import to_local_datetime


class BaseSchema(ma.ModelSchema):
    # TODO convert time to local time
    # created_at = fields.Method("to_local_created_datetime", dump_only=True, allow_none=False)
    # updated_at = fields.Method("to_local_updated_datetime", dump_only=True, allow_none=False)

    class Meta:
        unknown = EXCLUDE
        ordered = True

    @staticmethod
    def to_local_created_datetime(obj):
        if obj:
            return to_local_datetime(obj.created_at).strftime("%Y-%m-%d %H:%M:%S")
        return None

    @staticmethod
    def to_local_updated_datetime(obj):
        if obj:
            return to_local_datetime(obj.updated_at).strftime("%Y-%m-%d %H:%M:%S")
        return None