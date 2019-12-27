from flask import request
from flask_restful import Resource

from models import Message, Room, User, serialize_multiple
from utils.validator import ModelValidator


class Rooms(Resource):
    def get(self):
        return serialize_multiple(Room.query.all())

    def post(self):
        data = request.get_json()

        return ModelValidator(Room).post(data)


class RoomUsers(Resource):
    def get(self, room_id):
        return ModelValidator(Room).get_model_in_room_by_id(room_id)

    def post(self, room_id):
        user_id = request.get_json()['user_id']

        return ModelValidator(Room).post_model_in_room_by_id(room_id, user_id)


class RoomMessages(Resource):
    def get(self, room_id):
        return serialize_multiple(
            Message.query.filter(Message.room_id == room_id).all()
        )
