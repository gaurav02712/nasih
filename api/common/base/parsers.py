from datetime import datetime

from flask_restplus import reqparse

from apis.constants.common import LIMIT, OFFSET, DATE_FORMAT, LABEL_DATE

base_pagination_parser = reqparse.RequestParser()
base_pagination_parser.add_argument('offset', type=int, location='args', help='Index of the record to fetch from',
                                    default=OFFSET)
base_pagination_parser.add_argument('limit', type=int, location='args', help='Number of records to fetch',
                                    default=LIMIT)

# Report
base_report_parser = reqparse.RequestParser()
base_report_parser.add_argument('from_date',
                                type=lambda x: datetime.strptime(x, DATE_FORMAT),
                                help='From date ({})'.format(LABEL_DATE))
base_report_parser.add_argument('to_date',
                                type=lambda x: datetime.strptime(x, DATE_FORMAT),
                                help='To date ({})'.format(LABEL_DATE))
