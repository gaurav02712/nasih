from flask import jsonify
from api.helpers.response import ApiResponse


class InvalidUsage(Exception):
    status_code = 500

    def __init__(self, errors, status_code=500, payload=None):
        # db.session.rollback()
        Exception.__init__(self)
        self.errors = errors
        self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = self.errors
        return jsonify(rv)

    @classmethod
    def validationError(cls, error, status_code):
        print(status_code)
        error, code = ApiResponse.error(error=error, status_code=status_code, message='')
        return cls(errors=error, status_code=code)
