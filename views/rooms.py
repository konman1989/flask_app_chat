from flask import request
from flask_restful import Resource

from models import Message, Room, User, serialize_multiple
from settings import db


class Rooms(Resource):
    def get(self):
        return serialize_multiple(Room.query.all())

    def post(self):
        data = request.get_json()

        room = Room(**data)
        db.session.add(room)
        db.session.flush()

        room_id = room.id
        db.session.commit()

        return {"id": room_id}, 201


class RoomUsers(Resource):
    def get(self, room_id):
        return serialize_multiple(Room.query.get(room_id).users)

    def post(self, room_id):
        user_id = request.get_json()['user_id']
        room = Room.query.get(room_id)
        room.users.append(User.query.get(user_id))
        db.session.commit()

        return {}, 201


class RoomMessages(Resource):
    def get(self, room_id):
        return serialize_multiple(
            Message.query.filter(Message.room_id == room_id).all()
        )
