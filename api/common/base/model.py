from datetime import datetime
from api.helpers.database import SurrogatePK
from api.config.initialization import db


class BaseModel(db.Model, SurrogatePK):
    """  Use this class to models with default fields.  """
    __abstract__ = True
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    @classmethod
    def baseExcluded(cls):
        return ('is_deleted', 'created_at', 'created_by', 'updated_at')



