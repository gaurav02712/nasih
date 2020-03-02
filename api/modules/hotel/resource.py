from amadeus import ResponseError
from api.config.initialization import api, amadeus
from api.helpers.extension import Resource, cleanNullItems, list_to_csv
from api.helpers.jwt_helper import jwt_required
from api.helpers.response import ApiResponse
from api.modules.hotel.business import format_muslim_friendly_data, get_static_data
from api.modules.hotel.model import HotelModel, IATACodeModel

ns_hotel = api.namespace('hotel', description='Hotel Module')


class Hotel(Resource):
    parser = HotelModel().get_parser_hotel_filters()

    @ns_hotel.expect(parser)
    @ns_hotel.doc(security="Authorization")
    # @jwt_required
    def get(self):
        try:
            params = self.parser.parse_args()
            if params['childAges'] is not None:
                params['childAges'] = list_to_csv(params['childAges'])
            if params['ratings'] is not None:
                params['ratings'] = list_to_csv(params['ratings'])
            params = cleanNullItems(params)
            response = amadeus.shopping.hotel_offers.get(**params)
            mf_data = format_muslim_friendly_data(response.data)
            return ApiResponse.success(mf_data, 200)
        except ResponseError as error:
            print(f'Error is ----------{error}')
            return ApiResponse.error(error.response.body, 402)


class StaticData(Resource):
    parser = HotelModel().sample_parser()

    # @ns_hotel.doc(security="Authorization")
    # @jwt_required
    # @ns_hotel.expect(parser)
    def get(self):
        """Get Static data"""
        data = get_static_data()
        return ApiResponse.success(data, 200)


class IATACode(Resource):
    # @ns_hotel.doc(security="Authorization")
    # @jwt_required
    def get(self, keyword: str):
        """Search by keyword"""
        return {'status': "Need to do it."}
        # paginated_qwargs = pagination_kwargs(request)
        # # schema = CuisineSchema(many=True)
        # # page = paginated_qwargs['page']
        # # per_page = paginated_qwargs['limit']
        #
        # # name city country iata
        #
        # if keyword is None:
        #     records = IATACodeModel.query.paginate(page, per_page, False)
        # else:
        #     records = IATACodeModel.query.filter(IATACodeModel.name.like('{}%'.format(keyword))).paginate(page, per_page,
        #                                                                                                 False)
        # return ApiResponse.success(get_paginated_list(records, schema, page, per_page), 200)
        #
        #
        # # TODO :- need to implement this
        # data = get_static_data()
        # return ApiResponse.success(data, 200)
