"""Methods related to jwt, including encode, decode"""
import jwt
from base64 import b64decode
from django.conf import settings
import time
from random import randint


def decode_jwt(token):
    """Decodes the jwt token with ecrypted key from settings
    Returns the dict of data
    """
    # Removes some extra text
    token = token.replace('Bearer ', '')
    token = token.replace('Token ', '')
    try:
        result = jwt.decode(token, b64decode(settings.JWT_ENCRYPT_KEY))
    except jwt.exceptions.DecodeError:
        result = None
    return result


def encode_jwt(user_id, algorithm='HS256', exp_in_seconds=864000):
    """Create a jwt token with user_id. What is the jti?
    """

    iat = int(time.time())
    exp = iat + exp_in_seconds
    jti = iat + randint(9999, 999999)
    data = dict(jti=jti, sub=user_id, iat=iat, exp=exp)
    return jwt.encode(data, b64decode(settings.JWT_ENCRYPT_KEY), algorithm=algorithm)


def detect_lang(lang_header):
    lang = 'en'  # or vi
    if 'vi' in lang_header:
        lang = 'vi'
    return lang


def jwt_decode(token):
    return jwt.decode(token, b64decode(settings.JWT_ENCRYPT_KEY))

