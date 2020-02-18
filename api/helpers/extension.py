import flask_restplus
from flask import request
from flask_restplus.reqparse import RequestParser
from marshmallow import ValidationError

from api.config.initialization import ma
from api.helpers.exception import InvalidUsage


class Resource(flask_restplus.Resource):
    def validObject(self, parser: RequestParser, schema: ma.ModelSchema):
        json = parser.parse_args(request)
        return self.validObject_with_data(json, schema)

    def validObject_with_data(self, json_data, schema: ma.ModelSchema):
        # data, errors = schema.load(json_data)
        try:
            data = schema.load(json_data)
        except ValidationError as error:
            raise ValidationError(message=error.messages)
        # if errors:
        #     raise InvalidUsage.validationError(errors, 422)
        return data
