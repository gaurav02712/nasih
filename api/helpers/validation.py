from flask_restplus import ValidationError
from re import fullmatch

from api.helpers.exception import InvalidUsage


class Validation:
    def validate_phone(number: int):
        numberStr = str(number)
        if fullmatch('^[7986][0-9]{9}$', numberStr):
            return number
        raise InvalidUsage.validationError('Contact number must be a valid input', 422)

    def validate_name(name: str):
        def validate(s):
            if not len(s) >= 2 or not len(s) <= 50:
                raise ValidationError("{} must be 2 to 50 characters long" % name)

            if not fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,25})?', s):
                raise ValidationError('{} must be a valid input'.format(name))
            else:
                return s

        return validate

    def validate_length(name: str, required_length: int):
        def validate(s):
            if required_length == len(s):
                return s
            raise ValidationError("{} must be {} characters long".format(name, required_length))

        return validate

    def validate_min_max_length(name, min_len: int, max_len: int):
        def validate(s):
            if min_len <= len(s) <= max_len:
                return s
            raise ValidationError("{} must be {} to {} characters long".format(name, min_len, max_len))

        return validate

    def min_length(name: str, min_len: int):
        def validate(s):
            if len(s) >= min_len:
                return s
            raise ValidationError("{} must be at least {} characters long".format(name, min_len))

        return validate

    def max_length(name: str, max_len: int):
        def validate(s):
            if len(s) <= max_len:
                return s
            raise ValidationError("{} cannot be greater than {} characters".format(name, max_len))

        return validate
