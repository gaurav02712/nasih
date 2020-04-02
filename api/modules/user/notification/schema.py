from api.config.initialization import ma
from api.modules.user.notification.model import NotificaionModel


class NotificaionModelSchema(ma.ModelSchema):
    class Meta:
        model = NotificaionModel
