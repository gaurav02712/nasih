from amadeus import ResponseError
from api.config.initialization import api, amadeus
from api.helpers.extension import Resource, cleanNullItems
from api.helpers.jwt_helper import jwt_required
from api.helpers.response import ApiResponse
from api.modules.hotel.model import HotelModel

ns_hotel = api.namespace('hotel', description='Hotel Module')


class Hotel(Resource):
    parser = HotelModel().get_parser_hotel_filters()

    @ns_hotel.expect(parser)
    @ns_hotel.doc(security="Authorization")
    # @jwt_required
    def get(self):
        try:
            params = cleanNullItems(self.parser.parse_args())
            response = amadeus.shopping.hotel_offers.get(**params)
            return ApiResponse.success(response.data, 200)
        except ResponseError as error:
            print('Error is ----------')
            print(error)
            return ApiResponse.error('Something went wrong.', 402)
