from sqlalchemy import or_

from amadeus import ResponseError
from api.common.base.parsers import base_pagination_parser
from api.config.initialization import api, amadeus
from api.helpers.extension import Resource, cleanNullItems, list_to_csv
from api.helpers.jwt_helper import jwt_required
from api.helpers.pagination import get_paginated_list
from api.helpers.response import ApiResponse
from api.modules.hotel.business import format_muslim_friendly_data, get_static_data
from api.modules.hotel.model import HotelModel, IATACodeModel
from api.modules.hotel.schema import IATACodeModelSchema

ns_hotel = api.namespace('hotel', description='Hotel Module')


class Hotel(Resource):
    parser = HotelModel().get_parser_hotel_filters()

    @ns_hotel.expect(parser)
    @ns_hotel.doc(security="Authorization")
    @jwt_required
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


class HotelOffer(Resource):
    parser = HotelModel().get_parser_hotel_offers()

    @ns_hotel.expect(parser)
    @ns_hotel.doc(security="Authorization")
    @jwt_required
    def get(self):
        try:
            params = self.parser.parse_args()
            params = cleanNullItems(params)
            hotel_offers = amadeus.shopping.hotel_offers_by_hotel.get(**params)
            return ApiResponse.success(hotel_offers.data, 200)
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
    parser = IATACodeModel().get_parser_search()

    @ns_hotel.doc(security="Authorization")
    @jwt_required
    @ns_hotel.expect(parser)
    def get(self, keyword: str):
        """Search by keyword"""
        args = self.parser.parse_args()
        page = args.page
        per_page = args.limit
        if keyword is None:
            records = IATACodeModel.query.paginate(page=page, per_page=per_page)
        else:
            query = or_(IATACodeModel.name.ilike('{}%'.format(keyword)),
                        IATACodeModel.city.ilike('{}%'.format(keyword)),
                        IATACodeModel.country.ilike('{}%'.format(keyword)),
                        IATACodeModel.iata.ilike('{}%'.format(keyword)))
            records = IATACodeModel.query.filter(query).paginate(page, per_page, False)
        return ApiResponse.success(get_paginated_list(records, IATACodeModelSchema(many=True), per_page), 200)
