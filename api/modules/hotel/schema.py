from api.config.initialization import ma
from api.modules.hotel.model import HotelModel, CurrencyModel, IATACodeModel


class HotelSchema(ma.ModelSchema):
    class Meta:
        model = HotelModel
        include_fk = True
        exclude = model.baseExcluded()


class CurrencySchema(ma.ModelSchema):
    class Meta:
        model = CurrencyModel
        include_fk = True


class IATACodeModelSchema(ma.ModelSchema):
    class Meta:
        model = IATACodeModel
        include_fk = True
        exclude = model.baseExcluded()
