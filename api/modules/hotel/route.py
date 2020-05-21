from api.modules.hotel.resource import ns_hotel, Hotel, Hotels, StaticData, IATACode, HotelOffer, HotelBooking, FavHotels

ns_hotel.add_resource(Hotel, '/<string:hotel_code>')
ns_hotel.add_resource(Hotels, '/')
ns_hotel.add_resource(StaticData, '/staticdata')
ns_hotel.add_resource(IATACode, '/iata_code/<string:keyword>')
ns_hotel.add_resource(HotelOffer, '/offer/')
ns_hotel.add_resource(HotelBooking, '/booking/')
ns_hotel.add_resource(HotelBooking, '/booking/<string:booking_id>', methods=['GET'])

ns_hotel.add_resource(FavHotels, '/fav/', methods=['GET'])
ns_hotel.add_resource(FavHotels, '/fav/<string:entity_id>', methods=['POST'])
