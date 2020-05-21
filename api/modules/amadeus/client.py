import os
from uuid import uuid4

from lxml import etree
from zeep import Client, Settings, xsd

from api.modules.amadeus.helpers import CustomUsernameToken, output_formatter
from .constants import ActionURL, WSDLFilePath, TransactionStatusCode


class Amadeus:
    _client = None
    _settings = Settings(xsd_ignore_sequence_order=True, strict=True, forbid_entities=False)

    def __init__(self, formatter=output_formatter):
        # Todo: refactor code
        self.username = os.environ.get('AMADEUS_USERNAME')
        self.password = os.environ.get('AMADEUS_PASSWORD')
        self.office_id = os.environ.get('AMADEUS_OFFICE_ID')
        self.host = os.environ.get('AMADEUS_HOST')
        self.format = formatter

    def get_header(self, session_status=None, session_id=None, sequence_number=None, security_token=None):
        element_sequence = [
            xsd.Element(name='{http://www.w3.org/2005/08/addressing}MessageID', type_=xsd.String()),
            xsd.Element(name='{http://www.w3.org/2005/08/addressing}Action', type_=xsd.String()),
            xsd.Element(name='{http://www.w3.org/2005/08/addressing}To', type_=xsd.String()),
        ]
        if session_status in [TransactionStatusCode.IN_SERIES.value,
                              TransactionStatusCode.END.value]:
            element_sequence.append(
                xsd.Element(
                    '{http://xml.amadeus.com/2010/06/Session_v3}Session', type_=xsd.ComplexType(
                        xsd.Sequence([
                            xsd.Element(name='SessionId', type_=xsd.String()),
                            xsd.Element(name='SequenceNumber', type_=xsd.String()),
                            xsd.Element(name='SecurityToken', type_=xsd.String()),
                        ]),
                        attributes=[
                            xsd.Attribute('TransactionStatusCode', xsd.String())
                        ]

                    )
                )
            )

        if session_status not in [TransactionStatusCode.IN_SERIES.value, TransactionStatusCode.END.value]:
            element_sequence.append(
                xsd.Element(
                    '{http://xml.amadeus.com/2010/06/Security_v1}AMA_SecurityHostedUser', xsd.ComplexType(
                        xsd.Sequence([
                            xsd.Element(name='UserID', type_=xsd.ComplexType(
                                attributes=[
                                    xsd.Attribute('AgentDutyCode', xsd.String()),
                                    xsd.Attribute('RequestorType', xsd.String()),
                                    xsd.Attribute('PseudoCityCode', xsd.String()),
                                    xsd.Attribute('POS_Type', xsd.String())
                                ]
                            )),
                        ])
                    )
                )
            )
        if session_status == TransactionStatusCode.START.value:
            element_sequence.append(
                xsd.Element(
                    '{http://xml.amadeus.com/2010/06/Session_v3}Session', type_=xsd.ComplexType(
                        attributes=[
                            xsd.Attribute('TransactionStatusCode', xsd.String())
                        ]
                    )
                )
            )

        header = xsd.ComplexType(xsd.Sequence(element_sequence))

        header_data = {
            'MessageID': str(uuid4()),
            'Action': ActionURL.Hotel_MultiSingleAvailability,
            'To': self.host,
            **({'AMA_SecurityHostedUser': {
                'UserID': {
                    'AgentDutyCode': 'SU',
                    'RequestorType': 'U',
                    'PseudoCityCode': self.office_id,
                    'POS_Type': "1",
                }
            }} if session_status not in [TransactionStatusCode.IN_SERIES.value, TransactionStatusCode.END.value] else {}),

            **({
                'Session': {
                    'TransactionStatusCode': session_status
                }
            }if session_status == TransactionStatusCode.START.value else {}),

            **({
                   'Session': {
                       'SessionId': session_status,
                       'SequenceNumber': session_status,
                       'SecurityToken': session_status,
                       'TransactionStatusCode': session_status
                   }
               } if session_status in [
                TransactionStatusCode.IN_SERIES.value,
                TransactionStatusCode.END.value] else {}),
        }

        new_header_data = {k: v for k, v in header_data.items() if v is not None}
        header_data.clear()
        header_data.update(new_header_data)
        return header(**header_data)

        # return header_value

    def set_client(self, wsse=False):
        self._client = Client(
            wsdl=WSDLFilePath.HOTEL_AVAILABILITY_WSDL,
            wsse=CustomUsernameToken(username=self.username, password=self.password, use_digest=True) if wsse else None,
            settings=self._settings
        )

    @staticmethod
    def get_room_candidates(no_of_rooms, no_of_adults, child_ages=None, booking_code=None, room_type_code=None):
        return {
            'RoomStayCandidate': {
                **({'BookingCode': str(booking_code)} if booking_code is not None else {}),
                **({'RoomTypeCode': str(room_type_code)} if room_type_code is not None else {}),
                'Quantity': str(no_of_rooms),
                'RoomID': "1",
                'GuestCounts': {
                    'IsPerRoom': "true",
                    'GuestCount':
                        [
                            {
                                'Count': no_of_adults,
                                'AgeQualifyingCode': "10"
                            },


                            # {
                            #     'Age': "5",
                            #     'Count': "1",
                            #     'AgeQualifyingCode': "8"
                            # }
                        ],

                }
            }
        }

    def get_hotels(
            self, check_in_date: str, check_out_date: str, latitude: str, longitude: str, min_price=None,
            max_price=None, radius: str = "10",
            currency: str = "EUR", no_of_rooms: int = 1, no_of_adults: int = 1, child_ages: list = None,
            unit_of_measure: int = 2, hotel_name: str = None, city_code=None, limit: int = None, offset: int = 10
    ) -> dict:
        self.set_client(wsse=True)
        client = self._client
        # Todo:
        '''
        There are 4 Hotel Categories which can be requested. It is accomplished 
        using the following codes belonging to the OTA Group Segment Category Code:
            
            First Class Hotels (OTA Code = “7”)
            Luxury Hotels (OTA Code = “8”)
            Tourist Hotels (OTA Code = “13”)
            Standard Class Hotels (OTA Code = “16”)
            
        @DistanceMeasure: Indicates if the search should be sorted by distance or random
            DIS: sorted by distance
            RND: random
        
        2.25 Sub Structure: Search By Third Party Rating
        <Award Provider="LSR" Rating="3"/> //LSR stands for Local Star Rating
        
        Child Code 
        '''

        hotel_data = {
            'SearchCacheLevel': 'VeryRecent',  # c
            'EchoToken': 'MultiSingle',
            'SummaryOnly': "1",
            'RateRangeOnly': "1",
            'RateDetailsInd': "1",
            'AvailRatesOnly': "1",
            'RequestedCurrency': currency,
            'Version': "4.000",
            'PrimaryLangID': "EN",
            # 'MaxResponses': "10",
            'AvailRequestSegments': {
                'AvailRequestSegment': {
                    'InfoSource': 'Distribution',
                    'HotelSearchCriteria': {
                        'AvailableOnlyIndicator': "true",
                        'Criterion': {
                            **({
                                   'ExactMatch': "true",
                                   'HotelRef': {
                                       'HotelCityCode': str(city_code),
                                   }
                               } if city_code else {}
                               ),
                            **({'Position': {
                                'Latitude': str(latitude),
                                'Longitude': str(longitude)
                            }} if latitude and longitude else {}),

                            **({'Radius': {
                                'Distance': str(radius),  # Maximum 300
                                'UnitOfMeasureCode': str(unit_of_measure),  # 1 for Miles, 2 for Km
                                'DistanceMeasure': "DIS"
                            }} if latitude and longitude else {}),

                            'StayDateRange': {
                                'Start': str(check_in_date),
                                'End': str(check_out_date),
                            },

                            **({'RateRange': {
                                'CurrencyCode': currency,
                                'MaxRate': max_price,
                                'MinRate': min_price
                            }} if min_price and max_price else {}),

                            'RoomStayCandidates': self.get_room_candidates(no_of_rooms, no_of_adults, child_ages)
                        }
                    }
                }
            },
            '_soapheaders': [self.get_header()]
        }

        # hotel_data = request_param_formatter(params=hotel_data, input=locals())
        print('hotel_data')

        client.set_ns_prefix(None, "http://xml.amadeus.com/2010/06/Security_v1")
        node = client.create_message(client.service, 'Hotel_MultiSingleAvailability', **hotel_data)
        print('Hotel_MultiSingleAvailability', etree.tostring(node, pretty_print=True))
        response = client.service.Hotel_MultiSingleAvailability(**hotel_data)
        return self.format(response)
        # return {}

    def get_hotel(self, hotel_code: str, check_in_date: str, check_out_date: str, no_of_rooms: int = 1,
                  no_of_adults: int = 1, child_ages: list = None) -> dict:
        self.set_client(wsse=True)
        client = self._client
        # Todo:
        '''
        Child 
        '''

        hotel_data = {
            'SearchCacheLevel': 'Live',
            'EchoToken': 'MultiSingle',
            'SummaryOnly': "1",
            'RateRangeOnly': "1",
            'RateDetailsInd': "1",
            'AvailRatesOnly': "1",
            'RequestedCurrency': "EUR",
            'Version': "4.000",
            'PrimaryLangID': "EN",
            'AvailRequestSegments': {
                'AvailRequestSegment': {
                    'InfoSource': 'Distribution',
                    'HotelSearchCriteria': {
                        'AvailableOnlyIndicator': "true",
                        'Criterion': [
                            {
                                'StayDateRange': {
                                    'Start': str(check_in_date),
                                    'End': str(check_out_date),
                                },
                                'RoomStayCandidates': self.get_room_candidates(no_of_rooms, no_of_adults, child_ages)
                            },
                            {
                                'ExactMatch': "true",
                                'HotelRef': {
                                    'HotelCode': hotel_code
                                }
                            }
                        ]
                    }
                }
            },
            '_soapheaders': [self.get_header(session_status=TransactionStatusCode.START.value)]
        }

        client.set_ns_prefix(None, "http://xml.amadeus.com/2010/06/Security_v1")
        # node = client.create_message(client.service, 'Hotel_MultiSingleAvailability', **hotel_data)
        response = client.service.Hotel_MultiSingleAvailability(**hotel_data)
        return self.format(response)

    def get_hotel_pricing(self, session_id: str, security_token: str, check_in_date: str, check_out_date: str, hotel_code: str, chain_code: str,
                          hotel_city_code: str, rate_plan_code: str, booking_code: str, room_type_code: str,
                          no_of_rooms: int = 1, no_of_adults: int = 1, child_ages: list = None) -> dict:
        self.set_client()
        client = self._client
        # Todo:
        '''
        Child 
        '''

        hotel_data = {
            'EchoToken': 'Pricing',
            'SummaryOnly': "false",
            'RateRangeOnly': "false",
            'Version': "4.000",
            'AvailRequestSegments': {
                'AvailRequestSegment': {
                    'InfoSource': 'Distribution',
                    'HotelSearchCriteria': {
                        'AvailableOnlyIndicator': "true",
                        'Criterion': {
                            'ExactMatch': "true",
                            'HotelRef': {
                                'ChainCode': chain_code,
                                'HotelCode': hotel_code,
                                'HotelCityCode': hotel_city_code,
                            },
                            'StayDateRange': {
                                'Start': check_in_date,
                                'End': check_out_date,
                            },
                            'RatePlanCandidates': {
                                'RatePlanCandidate': {
                                    'RatePlanCode': rate_plan_code
                                }
                            },
                            'RoomStayCandidates': self.get_room_candidates(
                                no_of_rooms, no_of_adults, child_ages, booking_code, room_type_code
                            )
                        }
                    }
                }
            },
            '_soapheaders': [self.get_header(
                session_status=TransactionStatusCode.IN_SERIES.value, session_id=session_id,
                sequence_number=2, security_token=security_token
            )]
        }

        # node3 = client.create_message(client.service, 'Hotel_EnhancedPricing', **hotel_data)
        response = client.service.Hotel_EnhancedPricing(**hotel_data)
        return self.format(response)


amadeus_client = Amadeus()
