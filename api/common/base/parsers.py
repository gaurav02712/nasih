from flask_restplus import reqparse
from api.config.constants import K

base_pagination_parser = reqparse.RequestParser()

base_pagination_parser.add_argument('page', type=int, location='args', help='Page no to fetch data',
                                    default=K.PAGINATION_PAGE)
# base_pagination_parser.add_argument('offset', type=int, location='args', help='Index of the record to fetch from',
#                                     default=K.PAGINATION_OFFSET)
base_pagination_parser.add_argument('limit', type=int, location='args', help='Number of records to fetch',
                                    default=K.PAGINATION_PER_PAGE)
