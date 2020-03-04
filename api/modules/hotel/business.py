from flask import jsonify

from api.config.initialization import db


def format_muslim_friendly_data(data: dict) -> dict:
    return data


def get_amenities() -> list:
    return [
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


def get_currency_code() -> list:
    from api.modules.hotel.model import CurrencyModel
    currency = CurrencyModel().query.all()
    from api.modules.hotel.schema import CurrencySchema
    return CurrencySchema(many=True).dump(currency)


def get_static_data() -> dict:
    ratings = [5, 4, 3, 2, 1]
    amenities = get_amenities()
    currency = get_currency_code()
    return {'ratings': ratings, 'amenities': amenities, 'currency': currency}
