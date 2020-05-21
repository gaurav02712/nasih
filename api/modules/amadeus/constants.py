import os
from enum import Enum

basedir = os.path.abspath(os.path.dirname(__file__))
wsdl_dir = os.path.join(basedir, '../../.././wsdl/1ASIWMUSAYK_PDT_20200504_074141/')


class WSDLFilePath(object):
    HOTEL_AVAILABILITY_WSDL = os.path.join(wsdl_dir, '1ASIWMUSAYK_PDT_HotelAvailability_2.0_4.0.wsdl')


class ActionURL(object):
    Hotel_MultiSingleAvailability = 'http://webservices.amadeus.com/Hotel_MultiSingleAvailability_10.0'


class TransactionStatusCode(Enum):
    START = 'Start'
    IN_SERIES = 'InSeries'
    END = 'End'



