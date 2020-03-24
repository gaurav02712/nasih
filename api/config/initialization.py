import os

from flask import Blueprint
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, Model
from flask_restplus import Api
from flask_bcrypt import Bcrypt
from amadeus import Client, ResponseError
from flask_mail import Mail

from api.config.jwt_configuration import check_if_token_in_blacklist, add_claims_to_access_token, user_identity_lookup


class CrudMethods(Model):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True, slug=False):
        """Save the record."""
        if hasattr(self, 'alias'):
            self.alias = get_unique_slug(self)
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        # db.session.delete(self)
        if hasattr(self, 'is_deleted'):
            self.is_deleted = True
        return commit and self.save() or self


authorizations = {
    'Authorization': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

# app = Flask(__name__)
db = SQLAlchemy(model_class=CrudMethods)
ma = Marshmallow()
migrate = Migrate()
blueprint = Blueprint('AirOrder', __name__, url_prefix='/v1')
api = Api(blueprint, authorizations=authorizations, title='Nasih', doc='/api/doc/', version='1.0.0',
          description='')
bcrypt = Bcrypt()
amadeus = Client(
    client_id=os.environ.get('AMADEUS_CLIENT_ID'),
    client_secret=os.environ.get('AMADEUS_CLIENT_SECRET'),
    hostname=os.environ.get('AMADEUS_ENVIROMENT'))
mail = Mail()

# jwt class
jwt = JWTManager()
jwt.token_in_blacklist_loader(check_if_token_in_blacklist)
jwt.user_claims_loader(add_claims_to_access_token)
jwt.user_identity_loader(user_identity_lookup)
jwt._set_error_handler_callbacks(api)


# def check_if_token_in_blacklist(decrypted_token):
#     jti = decrypted_token['jti']
#
# #  return RevokedTokenModel.is_jti_blacklisted(jti)
#
# def add_claims_to_access_token(user):
#     return {'roles': user.user_role.role_id}
#
#
# def user_identity_lookup(user):
#     return {'username': user.username, 'user_id': user.id, 'user_type': user.type}


def prepare_libraries(app):
    # bcrypt.init_app(app)
    # cache.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)


def register_header(app):
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response


def get_unique_slug(self):
    """
    Takes a model instance, sluggable field name (such as 'title') of that
    model as string, slug field name (such as 'slug') of the model as string;
    returns a unique slug as string.
    """
    from slugify import slugify
    unique_slug = slugify(self.name)
    extension = 1
    ModelClass = self.__class__
    while ModelClass.query.filter_by(**{'alias': unique_slug}).count():
        unique_slug = '{}-{}'.format(unique_slug, extension)
        extension += 1

    return unique_slug
