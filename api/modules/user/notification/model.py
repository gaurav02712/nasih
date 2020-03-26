from api.common.base.model import BaseModel
from api.config.initialization import db


class NotificaionModel(BaseModel):
    __tablename__ = 'notification'
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), unique=True)
    # sender_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), unique=True)
    is_seen = db.Column(db.Boolean, nullable=False, default=0)
    is_viewed = db.Column(db.Boolean, nullable=False, default=0)
    type = db.Column(db.Integer, nullable=False, default=0)
    entity_id = db.Column(db.Integer, nullable=True, default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_parser_fetch_notification(cls):
        from api.common.base.parsers import base_pagination_parser
        parser = base_pagination_parser.copy()
        return parser
