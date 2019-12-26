from flask import request
from flask_restful import Resource

from models import Message, serialize_multiple
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

        message = Message(**data)
        db.session.add(message)
        db.session.flush()

        message_id = message.id
        db.session.commit()

        return {"id": message_id}, 201


class SingleMessage(Resource):
    def get(self, message_id):
        return Message.query.get(message_id).serialize()

    def patch(self, message_id):
        data = request.get_json()
        db.session.query(Message).filter_by(id=message_id).update(data)
        db.session.commit()

        return 204

    def delete(self, message_id):
        db.session.query(Message).filter_by(id=message_id).delete()
        db.session.commit()
        return 200
