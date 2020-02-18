from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from sqlalchemy.exc import SQLAlchemyError

from api.config.initialization import db
import re

from api.helpers.response import ApiResponse


def handle_integrity_error(exc):
    db.session.rollback()
    msg = exc.args[0].split('Key')
    message = re.sub(u'[()\\n]', '', msg[-1])
    message = re.sub(u'[=]', ' ', message)
    return ApiResponse.error(exc.args, 409, message, error_type=exc.__class__.__name__)


def handle_invalid_request_error(exc):
    db.session.rollback()
    msg = exc.args[0].split('Key')
    message = re.sub(u'[()\\n]', '', msg[-1])
    message = re.sub(u'[=]', ' ', message)
    status_code = 409
    response = {
        'success': "error",
        'error': {
            'type': exc.__class__.__name__,
            'message': message
        },
        'data': ''
    }
    return jsonify(response), status_code


def exception_handler(error):
    db.session.rollback()
    return jsonify({'Exception': error.args[0]}), 500
    # response = error.to_json()
    # response.status_code = error.status_code


def schema_validation_error(exc):
    error_type_name = type(exc).__name__
    return ApiResponse.error(error=exc.messages, status_code=422, error_type=error_type_name)


def sqlalchemy_error_handler(exc):
    error_type_name = type(exc).__name__
    error_message = str(exc.__dict__['orig'])
    return ApiResponse.error(error=error_message, status_code=422, error_type=error_type_name, message=error_message)


def register_error_handlers(app):
    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    # app.errorhandler(InvalidUsage)(errorhandler)
    app.register_error_handler(IntegrityError, handle_integrity_error)
    # app.register_error_handler(404, handle_object_not_found)
    app.register_error_handler(InvalidRequestError, handle_invalid_request_error)
    app.register_error_handler(ValidationError, schema_validation_error)

    app.register_error_handler(SQLAlchemyError, sqlalchemy_error_handler)
    # TODO:- Can we use above one for globally expection
