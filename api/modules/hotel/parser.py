from flask_restplus import reqparse

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

get_hotel_parser = reqparse.RequestParser(bundle_errors=True, trim=True)
# get_hotel_parser.add_argument('hotel_code', type=str, required=True, help='Hotel identifier code', location='form')

get_hotel_parser.add_argument(
    'check_in_date', type=str, required=True,
    help='''Format YYYY-MM-DD. The lowest accepted value is the present date (no dates in the past). 
    If not present, the default value will be todays date in the GMT timezone.''', location='form'
)
get_hotel_parser.add_argument(
    'check_out_date', type=str, required=True,
    help='The lowest accepted value is check_in_date + 1', location='form'
)
get_hotel_parser.add_argument('no_of_rooms', type=int, required=True, help='number of rooms (1-9)', location='form')
get_hotel_parser.add_argument('no_of_adults', type=int, required=True, help='number of adult guests (1-9) per room', location='form')
get_hotel_parser.add_argument(
    'child_ages', type=int, required=False, default=None, action='split',
    help='''comma separated list of ages of each child. If several children have the same  age, their ages should be 
    repeated in the list''', location='form'
)


get_hotels_parser = get_hotel_parser.copy()
# get_hotels_parser.remove_argument('hotel_code')
# get_hotels_parser.replace_argument('hotel_code', type=str, help='Hotel identifier code', location='form')
get_hotels_parser.add_argument('city_code', type=str, required=False, help='city IATA code', location='form')

get_hotels_parser.add_argument(
    'hotel_name', type=str,
    help='''Search by Hotel Name. Accepts maximum 4 keywords.''', location='form'
)
get_hotels_parser.add_argument('min_price', type=float, help='Minimum budget', location='form')
get_hotels_parser.add_argument('max_price', type=float, help='Maximum budget', location='form')
get_hotels_parser.add_argument('radius', type=int, default=10, location='form')
get_hotels_parser.add_argument(
    'unit_of_measure', type=int, default=1, choices=[1, 2],
    help='Measure unit for radius. 1 for KM, 2 for Miles', location='form'
)
get_hotels_parser.add_argument('latitude', type=str, location='form')
get_hotels_parser.add_argument('longitude', type=str, location='form')
get_hotels_parser.add_argument('currency', type=str, help='''ISO currency code''', location='form')
get_hotels_parser.add_argument('limit', type=int, default=5, help='''maximum number of hotels in each response''', location='form')
get_hotels_parser.add_argument('offset', type=int, default=1, location='form')
# get_hotels_parser.add_argument('amenities', choices=amenities, action='append', location='form')
# get_hotels_parser.add_argument(
#     'ratings', type=list, choices=[5, 4, 3, 2, 1], help='''hotel stars. Up to four values can be requested at the same
#     time in a comma separated list''', action='append', location='form'
# )


hotel_pricing_parser = get_hotel_parser.copy()
hotel_pricing_parser.add_argument('session_id', type=str, required=True, location='form')
hotel_pricing_parser.add_argument('security_token', type=str, required=True, location='form')
hotel_pricing_parser.add_argument('hotel_city_code', type=str, required=True, location='form')
hotel_pricing_parser.add_argument('hotel_chain_code', type=str, required=True, location='form')
hotel_pricing_parser.add_argument('hotel_rate_plan_code', type=str, required=True, location='form')
hotel_pricing_parser.add_argument('booking_code', type=str, required=True, location='form')
hotel_pricing_parser.add_argument('room_type_code', type=str, required=True, location='form')

