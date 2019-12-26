from __future__ import annotations
from sqlalchemy import or_

from settings import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"),
                          nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"))
    text = db.Column(db.String(2000), nullable=False)

    sender = db.relationship("User", foreign_keys=[sender_id])
    receiver = db.relationship("User", foreign_keys=[receiver_id])

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "room_id": self.room_id,
            "text": self.text
        }

    @staticmethod
    def fetch_private_conversation(sender_id, receiver_id):
        return db.session.query(Message)\
            .filter(or_(Message.sender_id == sender_id,
                        Message.receiver_id == sender_id))\
            .filter(or_(Message.receiver_id == receiver_id,
                        Message.sender_id == receiver_id))\
            .all()


room_users_table = db.Table(
    "room_users", db.Model.metadata,
    db.Column('room_id', db.Integer, db.ForeignKey("rooms.id")),
    db.Column('user_id', db.Integer, db.ForeignKey("users.id"))
)


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship(
        "User",
        secondary=room_users_table,
        backref="rooms"
    )
    messages = db.relationship("Message", backref="room")
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": str(self.created_at)
        }


def serialize_multiple(objects: list) -> list:
    return [obj.serialize() for obj in objects]


if __name__ == '__main__':
    db.create_all()
