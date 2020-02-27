from api.common.base.model import BaseModel



class HotelModel(BaseModel):
    __tablename__ = 'hotel'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

