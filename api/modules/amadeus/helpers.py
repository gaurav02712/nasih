import base64
import datetime
import decimal
import hashlib
import json
import os

import pytz
from zeep import ns, helpers
from zeep.wsse import UsernameToken, utils


def default(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    elif isinstance(obj, (datetime.date, datetime.time)):
        return obj.isoformat()
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)


def request_param_formatter(params: dict, input: dict) -> dict:
    for key in input.keys():
        if input[key] is None:
            del params[key]
    return params


class CustomUsernameToken(UsernameToken):
    def __init__(self, username, password, use_digest=False):
        UsernameToken.__init__(self, username=username, password=password, use_digest=use_digest)

    @staticmethod
    def get_timestamp(timestamp=None):
        timestamp = timestamp or datetime.datetime.utcnow()
        timestamp = timestamp.replace(tzinfo=pytz.utc)
        return timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    def apply(self, envelope, headers):
        security = utils.get_security_header(envelope)
        token = security.find("{%s}UsernameToken" % ns.WSSE)
        if token is None:
            token = utils.WSSE.UsernameToken()
            security.append(token)

        if self.timestamp_token is not None:
            security.append(self.timestamp_token)

        # Create the sub elements of the UsernameToken element
        elements = [utils.WSSE.Username(self.username)]
        if self.password is not None or self.password_digest is not None:
            if self.use_digest:
                elements.extend(self._create_password_digest())
            else:
                elements.extend(self._create_password_text())

        token.extend(elements)
        return envelope, headers

    def _create_password_digest(self):
        if self.nonce:
            nonce = self.nonce.encode("utf-8")
        else:
            nonce = base64.b64encode(os.urandom(16))
        timestamp = self.get_timestamp(self.created)
        hash_digest = hashlib.sha1()
        hash_digest.update(self.password.encode("utf-8"))

        # digest = Base64 ( SHA-1 ( nonce + created + password ) )
        if not self.password_digest:
            digest = base64.b64encode(
                hashlib.sha1(
                    base64.b64decode(nonce) + timestamp.encode("utf-8") + hash_digest.digest()
                ).digest()
            ).decode("ascii")
        else:
            digest = self.password_digest

        return [
            utils.WSSE.Password(
                digest, Type="%s#PasswordDigest" % self.username_token_profile_ns
            ),
            utils.WSSE.Nonce(
                nonce.decode("utf-8"),
                EncodingType="%s#Base64Binary" % self.soap_message_secutity_ns,
            ),
            utils.WSU.Created(timestamp),
        ]


def output_formatter(obj, get_session=True):

    # body = obj['body']
    # if get_session:
    #     session = obj['header']['session']
    #
    # obj = helpers.serialize_object(obj)
    # return json.loads(json.dumps(obj, default=default))

    return {
        'body': json.loads(json.dumps(helpers.serialize_object(obj['body']), default=default)),
        'session': json.loads(json.dumps(helpers.serialize_object(obj['header']['session']), default=default)) if get_session else None
    }
