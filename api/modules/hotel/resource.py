from flask import g
from sqlalchemy import or_

from amadeus import ResponseError

from api.common import KMessages
from api.common.base.parsers import base_pagination_parser
from api.config.initialization import api, amadeus
from api.helpers.extension import Resource, cleanNullItems, list_to_csv
from api.helpers.jwt_helper import jwt_required
from api.helpers.pagination import get_paginated_list
from api.helpers.response import ApiResponse
from api.modules.hotel.business import format_muslim_friendly_data, get_static_data
from api.modules.hotel.model import HotelModel, IATACodeModel, BookingModel, FavEntityModel
from api.modules.hotel.schema import IATACodeModelSchema, HotelBookingSchema, FavEntitySchema
from api.modules.amadeus import AmadeusClient
from .parser import get_hotel_parser, get_hotels_parser

ns_hotel = api.namespace('hotels', description='Hotel Module')


class Hotel(Resource):
    # parser = HotelModel().get_parser_hotel_filters()

    @ns_hotel.expect(get_hotel_parser)
    # @ns_hotel.doc(security="Authorization")
    # @jwt_required
    def post(self, hotel_code):
        try:
            params = get_hotel_parser.parse_args()
            params['hotel_code'] = hotel_code
            response = AmadeusClient.get_hotel(**params)
            return ApiResponse.success(response, 200)
        except ResponseError as error:
            print(f'Error is ----------{error}')
            return ApiResponse.error(error.response.body, 402)


class Hotels(Resource):
    # parser = HotelModel().get_parser_hotel_filters()

    @ns_hotel.expect(get_hotels_parser)
    # @ns_hotel.doc(security="Authorization")
    # @jwt_required
    def post(self):
        try:
            params = get_hotels_parser.parse_args()
            if (params.latitude is None or params.longitude is None) and params.city_code is None:
                return ApiResponse.error(None, 400, message=KMessages.LOCATION_OR_CITY_REQUIRED)
            response = AmadeusClient.get_hotels(**params)
            return ApiResponse.success(response, 200)
        except ResponseError as error:
            print(f'Error is ----------{error}')
            return ApiResponse.error(error.response.body, 402)


class HotelOffer(Resource):
    parser = HotelModel().get_parser_hotel_offers()

    @ns_hotel.expect(parser)
    @ns_hotel.doc(security="Authorization")
    @jwt_required
    def get(self):
        """All offer provided by a specific hotels"""
        try:
            params = self.parser.parse_args()
            params = cleanNullItems(params)
            hotel_offers = amadeus.shopping.hotel_offers_by_hotel.get(**params)
            return ApiResponse.success(hotel_offers.data, 200)
        except ResponseError as error:
            print(f'Error is ----------{error}')
            return ApiResponse.error(error.response.body, 402)


class HotelBooking(Resource):
    booking_parser = base_pagination_parser.copy()
    @ns_hotel.expect(booking_parser)
    @ns_hotel.doc(security="Authorization")
    # @jwt_required
    def get(self, booking_id: str = None):
        """Get user booking lisitng and booking with booking_id"""
        if booking_id is not None:
            booking_detail = BookingModel.query.filter(BookingModel.booking_id == booking_id).first()
            return ApiResponse.success(HotelBookingSchema().dump(booking_detail), 200)
        else:
            args = self.booking_parser.parse_args()
            page = args.page
            per_page = args.limit
            records = BookingModel.query.filter(BookingModel.user_id == g.user_id).paginate(page, per_page, False)
            return ApiResponse.success(get_paginated_list(records, HotelBookingSchema(many=True), per_page), 200)

    parser = BookingModel().get_parser_booking()

    # offerId = ''
    # guest name and contact
    @ns_hotel.expect(parser)
    @ns_hotel.doc(security="Authorization")
    @jwt_required
    def post(self):
        """Book specific hotels"""
        try:
            params = self.parser.parse_args()

            offerId = params['offerId']
            guests: list = params['guests']
            payments = params['payments']
            booking_response = amadeus.booking.hotel_bookings.post(offerId, guests, payments)
            booking_dict = booking_response.data[0]
            booking: BookingModel = BookingModel()
            booking.booking_id = booking_dict['id']
            booking.providerConfirmationId = booking_dict['providerConfirmationId']
            booking.user_id = g.user_id
            booking.hotel_name = params['hotel_name']
            booking.checking_date = params['checking_date']
            booking.checkout_date = params['checkout_date']
            booking.number_of_guest = len(guests)
            booking.number_of_room = params['number_of_room']
            booking.city = params['city']
            booking.address = params['address']
            booking.save()

            return ApiResponse.success(booking_dict, 200)
        except ResponseError as error:
            print(f'Error is ----------{error}')
            return ApiResponse.error(error.response.body, 402)


class FavHotels(Resource):
    parser = base_pagination_parser.copy()

    @ns_hotel.expect(parser)
    @ns_hotel.doc(security="Authorization")
    @jwt_required
    def get(self):
        """Get all Fav hotels id (Have to call seprterly Hotel Detail api for their details)"""
        page = self.parser.parse_args()['page']
        favorites = FavEntityModel.find_all(**{'pagination': True, 'page': page, 'user_id': g.user_id})
        return ApiResponse.success(get_paginated_list(favorites, FavEntitySchema(many=True), page), 200)

    @ns_hotel.doc(security='Authorization')
    @jwt_required
    def post(self, entity_id: str = None):
        """Mark fav any hotel (This will toggel fav/unfav a hotel))"""
        entity_type = 0
        fav_product = FavEntityModel.query.filter_by(user_id=g.user_id, entity_id=entity_id,
                                                     entity_type=entity_type).first()
        is_mark_fav = False
        if fav_product is not None:
            fav_product.delete()
        else:
            FavEntityModel(entity_id=entity_id, user_id=g.user_id, entity_type=entity_type).save()
            is_mark_fav = True
        return ApiResponse.success({'is_mark_fav': is_mark_fav}, 200, KMessages.UPDATED_SUCESSFULLY)


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
        """Search IATA code of an airport by country/city/airport/iata code"""
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
