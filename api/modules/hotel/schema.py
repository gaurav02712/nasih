from api.config.initialization import ma
from api.modules.hotel.model import HotelModel


class HotelSchema(ma.ModelSchema):

    class Meta:
        model = HotelModel
        include_fk = True
        exclude = model.baseExcluded()
