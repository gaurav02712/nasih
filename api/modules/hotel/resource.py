from api.config.initialization import api
from api.helpers.extension import Resource
from api.helpers.jwt_helper import jwt_required
from api.helpers.response import ApiResponse

ns_hotel = api.namespace('hotel', description='Hotel Module')


class Hotel(Resource):
    @ns_hotel.doc(security="Authorization")
    @jwt_required
    def get(self):
        return ApiResponse.error('Not implemented', 402)

