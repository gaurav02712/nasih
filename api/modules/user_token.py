from datetime import datetime, timedelta
from api.common.base.model import BaseModel
from api.config.initialization import db


class UserToken(BaseModel):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'user_token'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id', ondelete='CASCADE'))
    token = db.Column(db.String(1000), unique=True, nullable=False)
    refresh_token = db.Column(db.String(1000), unique=True, nullable=False)
    expired_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, token, refresh_token, user_id: int):
        self.user_id = user_id
        self.token = token
        self.refresh_token = refresh_token
        self.expired_at = datetime.utcnow() + timedelta(days=365)

    def __repr__(self):
        return '<UserToken: token: {}>'.format(self.token)

    @classmethod
    def is_token_valid(cls, auth_token):
        res = cls.query.filter(cls.token == auth_token,
                               cls.expired_at >= datetime.utcnow(),
                               cls.is_deleted == False).first()
        return res if True else False

    @classmethod
    def delete_token(cls, auth_token):
        user_token = cls.query.filter_by(token=auth_token).first()
        if user_token:
            user_token.is_deleted = True
            user_token.expired_at = datetime.utcnow()
            user_token.update()
