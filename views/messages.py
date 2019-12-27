from flask import request
from flask_restful import Resource

from models import Message, serialize_multiple
from utils.validator import ModelValidator
from settings import db


class Messages(Resource):
    def get(self):
        sender_id = request.args.get("sender_id")
        receiver_id = request.args.get("receiver_id")

        return serialize_multiple(
            Message.fetch_private_conversation(sender_id, receiver_id)
        )

    def post(self):
        data = request.get_json()

        return ModelValidator(Message).post(data)


class SingleMessage(Resource):
    def get(self, message_id):
        return ModelValidator(Message).get_by_id(message_id)

    def patch(self, message_id):
        data = request.get_json()

        return ModelValidator(Message).patch_by_id(message_id, data)

    def delete(self, message_id):
        db.session.query(Message).filter_by(id=message_id).delete()
        db.session.commit()
        return 200
