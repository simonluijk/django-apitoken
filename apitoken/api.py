
import hmac
from uuid import uuid4
from hashlib import sha256
from datetime import timedelta
from django.utils.timezone import now
from django.core.cache import cache
from .conf import TOKEN_TYPES


def _getkey(token):
    return 'apitoken-{}'.format(token)


class Token(object):

    def __init__(self, user, typ, token=None, expires=None):
        self.user = user
        self.typ = typ
        if token is None:
            self.token = hmac.new(uuid4().bytes, digestmod=sha256).hexdigest()
        else:
            self.token = token
        self.life = [t['life'] for t in TOKEN_TYPES if t['key'] == self.typ][0]
        self.expires = expires

    @property
    def is_valid(self):
        return self.user.is_active and self.expires >= now()

    def delete(self):
        cache.delete(_getkey(self.token))

    def save(self):
        self.expires = now() + timedelta(seconds=self.life)
        data = {
            'user': self.user,
            'typ': self.typ,
            'expires': self.expires,
        }
        cache.set(_getkey(self.token), data, self.life)


class TokenAPI(object):

    def get(self, token):
        """
        Returns a valid token if it exists else False
        """

        data = cache.get(_getkey(token))
        if data:
            token = Token(token=token, **data)
            if token.is_valid:
                token.save()
                return token

    def create(self, user, typ=None):
        """
        Creates a new token for the given user and type
        """

        if typ is None:
            typ = TOKEN_TYPES[0]['key']

        if typ not in [t['key'] for t in TOKEN_TYPES]:
            raise Exception('Invalid type {}'.format(typ))

        token = Token(user=user, typ=typ)
        token.save()
        return token


for typ in TOKEN_TYPES:
    setattr(TokenAPI, typ['key'].replace('-', '_').upper(), typ['key'])
