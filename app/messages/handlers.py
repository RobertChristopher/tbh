from http import HTTPStatus

from tornado.escape import json_decode
from app.base import BaseHandler
from app.auth.jwt import jwt_required
from app.messages.schema import (PendingMessageSchema, MutualMessageSchema)
from app.presets.services import get_preset_by_code
from app.exceptions import ApiError


@jwt_required
class MessageHandler(BaseHandler):
    '''
    Base handler for the message resource
    '''

    def initialize(self, message_service):
        self.message_service = message_service

        self.FILTER_SERVICES = {
            'sent': self.message_service.get_sent_messages,
            'received': self.message_service.get_received_messages,
            'mutual': self.message_service.get_mutual_messages
        }

        self.FILTER_SERIALIZERS = {
            'sent': PendingMessageSchema,
            'received': PendingMessageSchema,
            'mutual': MutualMessageSchema
        }

    def get(self):
        '''Retrieve Message resource'''

        try:
            filter = self.get_argument("filter")
            filter_service = self.FILTER_SERVICES[filter]
        except:
            # Filter does not exist
            raise ApiError(reason='specified filter does not exist', status=404)

        results = filter_service(self.tbh_user_id)
        message_schema = self.FILTER_SERIALIZERS[filter](many=True)
        results = {'messages': message_schema.dump(results).data }

        self.write(results)
        self.set_status(int(HTTPStatus.OK))
        self.finish()

    def write_error(self, error, **kwargs):
        # Send error up to base handler
        BaseHandler.write_error(self, error, *kwargs)

    def post(self):
        '''Send message'''

        request_body = json_decode(self.request.body)
        receiver_phone_number = request_body['receiver_phone_number']
        message_text = get_preset_by_code(request_body['message_id'])

        self.message_service.send_message(sender_id=self.tbh_user_id,
            receiver_phone_number=receiver_phone_number, text=message_text)

        self.set_status(int(HTTPStatus.OK))
        self.finish()