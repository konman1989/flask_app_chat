from settings import app, api

from views.messages import Messages, SingleMessage
from views.rooms import Rooms, RoomMessages, RoomUsers
from views.users import Users, SingleUser


api.add_resource(Users, '/users')
api.add_resource(SingleUser, '/users/<int:user_id>')

api.add_resource(Rooms, '/rooms')
api.add_resource(RoomMessages, '/rooms/<int:room_id>/messages')
api.add_resource(RoomUsers, '/rooms/<int:room_id>/users')

api.add_resource(Messages, '/messages')
api.add_resource(SingleMessage, '/messages/<int:message_id>')


if __name__ == '__main__':
    app.run(debug=True)
