import json
import os

from amadeus import ResponseError

from api.config.initialization import amadeus
from api.modules.hotel.model import IATACodeModel


def fetch_data():
    dump_data = []
    iatacodes = IATACodeModel.query.filter(IATACodeModel.data_available.is_(None),
                                           IATACodeModel.data_extracted.is_(None)).all()
    for iatacode in iatacodes:
        cityCode = iatacode.iata
        params: dict = {'cityCode': cityCode, 'page[limit]': '1000'}
        try:
            response = amadeus.shopping.hotel_offers.get(**params)
            new_list = response.data
            if len(new_list) > 0:
                dump_data = dump_data + new_list
                iatacode: IATACodeModel = IATACodeModel.query.filter(IATACodeModel.iata == cityCode).first()
                update_dict = {'data_extracted': True, 'data_available': True}
                iatacode.update(**update_dict)
                if len(dump_data) > 1000:
                    break
                print(f'City Code {cityCode}\n')
        except ResponseError as error:
            iatacode: IATACodeModel = IATACodeModel.query.filter(IATACodeModel.iata == cityCode).first()
            update_dict = {'data_extracted': True, 'data_available': False}
            iatacode.update(**update_dict)
            print(f'Error is ----------{error}')

    if len(dump_data) > 0:
        print(f'Saving data for rows ----------{len(dump_data)}')
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "hoteldump.json")
        with open(json_url, 'w') as json_file:
            json.dump(dump_data, json_file)
