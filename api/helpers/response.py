from flask import Response


class ApiResponse:
    def __error_massage(error) -> str:
        errtype = type(error)
        if errtype == str:
            return str(error)
        elif errtype == dict:
            try:
                return "\n".join([str for errorList in dict(error).values() for str in errorList])
                # message = ""
                # for key, value in  error.items():
                #     message += '{} - {}'.format(key,value) + '\n'
                # return message
            except:
                return ""
        elif errtype == list:
            return error[0]
        elif errtype == BaseException:
            return error.args
        else:
            return "Somewent went wrong."

    # 2xx
    @staticmethod
    def success(data: dict = None, status_code=200, message: str = ""):
        return {'status': True, 'data': data, 'message': message}, status_code

    # 3xx
    @staticmethod
    def redirect(data, status_code, message: str = None):
        return {'status': 'redirect', 'data': data, 'message': message}, status_code

    # 4xx
    @staticmethod
    def error(error, status_code: int, message: str = None, error_type: str = None):
        return {'status': False,
                'error': error,
                'error_type': error_type,
                'data': None,
                'message': ApiResponse.__error_massage(error) if message is None else message}, status_code
