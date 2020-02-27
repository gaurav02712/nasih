from api.common.base.model import BaseModel


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
        parser.add_argument('childAges', type=list, required=False, action='split', help='''comma separated list of ages
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
        parser.add_argument('amenities', type=list, choices=amenities, action='append', required=False)
        ratings = [5, 4, 3, 2, 1]
        parser.add_argument('ratings', type=list, choices=ratings, help='''hotel stars. Up to four values can be 
        requested at the same time in a comma separated list''', action='append', required=False)
        return parser
