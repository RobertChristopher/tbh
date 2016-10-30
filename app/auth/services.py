import json
import datetime
from http import HTTPStatus

import jwt
from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest

from app.exceptions import AuthError
from config import Config


JWT_CONFIG = Config.JWT
JWT_SECRET_TOKEN = JWT_CONFIG['secret']
JWT_ALGORITHM = 'HS256'


class AuthService(object):

    '''
    Authentication service
    '''

    async def fetch_digits_provider(self, provider_url, auth_header):
        '''
        Fetch digits provider url and retrieve user account information.
        This method uses Tornado's underyling async http client to retrieve
        content asynchronously. Callback supplied will be called with data upon
        completion.
        '''

        self._http_client = AsyncHTTPClient()

        try:
            response = await self._http_client.fetch(
                HTTPRequest(provider_url, headers={'Authorization': auth_header}))
        except:
            raise AuthError('Error retrieving digits account')

        response_status = response.code

        if not response_status == HTTPStatus.OK:
            raise AuthError('Error retrieving digits account')

        return json_decode(response.body)


class JWTService(object):

    '''
    JWT Authentication service
    '''

    def __init__(self):
        pass

    def sign_jwt_token(self, payload):

        encoded_token = jwt.encode(payload, Config.JWT['secret'],
            algorithm=JWT_ALGORITHM).decode(encoding='utf8')


        return encoded_token