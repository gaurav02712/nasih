from api.common.base.model import BaseModel
from api.common.base.parsers import base_pagination_parser
from api.common.enums import BookingStatus
from api.config.initialization import db


class CurrencyModel(db.Model):
    __tablename__ = 'currency'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country = db.Column(db.String(45), nullable=False)
    currency = db.Column(db.String(45), nullable=False)
    code = db.Column(db.String(45), nullable=False)
    symbol = db.Column(db.String(45), nullable=False)


class IATACodeModel(BaseModel):
    __tablename__ = 'iata_code'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(90), nullable=False)
    city = db.Column(db.String(45), nullable=True)
    country = db.Column(db.String(45), nullable=False)
    iata = db.Column(db.String(4), nullable=False)
    iaco = db.Column(db.String(9), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timezone = db.Column(db.String(45), nullable=False)
    dst = db.Column(db.String(45), nullable=False)

    @classmethod
    def get_parser_search(cls):
        parser = base_pagination_parser.copy()
        return parser


class HotelModel(BaseModel):
    __tablename__ = 'hotel'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_parser_hotel_filters(cls):
        from flask_restplus import reqparse
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        # parser.add_argument('params', type=dict, required=True, help='parameters in json format', location='form')
        parser.add_argument('cityCode', type=str, required=False, help='city IATA code')
        parser.add_argument('checkInDate', type=str, required=False, help='''Format YYYY-MM-DD.
        The lowest accepted value is the present date (no dates in the past).
        If not present, the default value will be todays date in the GMT timezone.''')
        parser.add_argument('checkOutDate', type=str, required=False, help='The lowest accepted value is checkInDate+1')
        parser.add_argument('roomQuantity', type=int, required=False, help='number of rooms (1-9)')
        parser.add_argument('adults', type=int, required=False, help='number of adult guests (1-9) per room')
        parser.add_argument('childAges', type=int, required=False, action='split', help='''comma separated list of ages
        of each child.
        If several children have the same age, their ages should be repeated in the list''')
        parser.add_argument('hotelName', type=str, required=False, help='''Search by Hotel Name.
        Accepts maximum 4 keywords.''')
        parser.add_argument('priceRange', type=str, required=False, help='''filter hotel offers by price per night
        interval (ex: 200-300 or -300 or 100) It is mandatory to include a currency when this field is set
        Note: a margin of +/- 10% is applied on the daily price''')
        parser.add_argument('currency', type=str, required=False, help='''ISO currency code''')
        parser.add_argument('page[limit]', type=int, required=False, help='''maximum number of hotels in each 
        response''')
        parser.add_argument('page[offset]', type=str, required=False)
        amenities = [
            "CONVENTION_CTR",
            "MEETING_ROOMS",
            "ICE_MACHINES",
            "RESTAURANT",
            "HANDICAP_FAC",
            "ACC_TOILETS",
            "DIS_PARKG",
            "BABY-SITTING",
            "BEAUTY_PARLOUR",
            "CAR_RENTAL",
            "ELEVATOR",
            "EXCHANGE_FAC",
            "WIFI",
            "LAUNDRY_SVC",
            "SPA",
            "VALET_PARKING",
            "HAIRDRESSER",
            "SWIMMING_POOL",
            "AIR_CONDITIONING",
            "HAIR_DRYER",
            "MINIBAR",
            "MOVIE_CHANNELS",
            "ROOM_SERVICE",
            "TELEVISION",
            "SAFE_DEP_BOX",
            "FITNESS_CENTER"
        ]
        parser.add_argument('amenities', choices=amenities, action='append', required=False)
        ratings = [5, 4, 3, 2, 1]
        parser.add_argument('ratings', type=list, choices=ratings, help='''hotel stars. Up to four values can be 
        requested at the same time in a comma separated list''', action='append', required=False)
        return parser

    @classmethod
    def get_parser_hotel_offers(cls):
        from flask_restplus import reqparse
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('hotelId', type=str, required=True)
        parser.add_argument('checkInDate', type=str, required=False, help='''Format YYYY-MM-DD.
                   The lowest accepted value is the present date (no dates in the past).
                   If not present, the default value will be todays date in the GMT timezone.''')
        parser.add_argument('checkOutDate', type=str, required=False, help='The lowest accepted value is checkInDate+1')
        parser.add_argument('roomQuantity', type=int, required=False, help='number of rooms (1-9)')
        parser.add_argument('adults', type=int, required=False, help='number of adult guests (1-9) per room')
        parser.add_argument('childAges', type=int, required=False, action='split', help='''comma separated list of ages
                  of each child.''')
        return parser

    @classmethod
    def sample_parser(cls):
        from flask_restplus import reqparse
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        return parser


# class BookingAssociatedRecords(db.Model):
#     __tablename__ = 'associated_record'


class BookingModel(BaseModel):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    booking_id = db.Column(db.String(45), nullable=False)
    providerConfirmationId = db.Column(db.String(45), nullable=False)  # GDS Confirmation Number. If you call the
    # Provider, this Reference may be asked
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # associated_record =

    hotel_name = db.Column(db.String(45), nullable=False)
    checking_date = db.Column(db.DateTime, nullable=False)
    checkout_date = db.Column(db.DateTime, nullable=False)
    number_of_guest = db.Column(db.Integer, nullable=False)
    number_of_room = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(45), nullable=False)
    booking_status = db.Column(db.Integer, nullable=False, default=BookingStatus.CONFIRM.value)  # booking_status

    # @classmethod
    # def save_booking_info(cls, data: dict, ):
    #     booking = BookingModel(**data)

    @classmethod
    def _get_parser_hotel_booking_details(cls):
        from flask_restplus import reqparse
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('hotel_name', type=str, required=True)
        parser.add_argument('checking_date', type=str, required=True, help='Date Of Birth (YYYY-MM-DD)')
        parser.add_argument('checkout_date', type=str, required=True, help='Date Of Birth (YYYY-MM-DD)')
        # parser.add_argument('number_of_guest', type=str, required=True)
        parser.add_argument('number_of_room', type=str, required=True)
        parser.add_argument('city', type=str, required=True)
        parser.add_argument('address', type=str, required=True)
        return parser

    @classmethod
    def get_parser_booking(cls):
        from flask_restplus import reqparse
        parser = BookingModel._get_parser_hotel_booking_details()
        parser.add_argument('offerId', type=str, required=True)
        guests = '''sample - [
                      {
                        "name": {
                          "title": "MR",
                          "firstName": "BOB",
                          "lastName": "SMITH"
                        },
                        "contact": {
                          "phone": "+33679278416",
                          "email": "bob.smith@email.com"
                        }
                      }
                    ]'''

        parser.add_argument('guests', type=list, required=True, location='json', help=guests)
        payments = '''{ "payments": [
    {
      "method": "creditCard",
      "card": {
        "vendorCode": "VI",
        "cardNumber": "4111111111111111",
        "expiryDate": "2023-01"
      }
    }
  ]}'''
        parser.add_argument('payments', type=list, required=False, location='json', help=payments)

        help = '''offerId, guests, payments and 
        optional rooms for the repartition (when used the rooms array items must match the shopping offer 
        roomQuantity)'''
        return parser
