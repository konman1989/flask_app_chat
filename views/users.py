from flask import request
from flask_restful import Resource

from models import User, serialize_multiple
from utils.validator import ModelValidator
from settings import db


class Users(Resource):
    def get(self):
        return serialize_multiple(User.query.all())

    def post(self):
        data = request.get_json()

        return ModelValidator(User).post(data)


class SingleUser(Resource):
    def get(self, user_id):
        return ModelValidator(User).get_by_id(user_id)

    def patch(self, user_id):
        data = request.get_json()
        return ModelValidator(User).patch_by_id(user_id, data)

    def delete(self, user_id):
        db.session.query(User).filter_by(id=user_id).delete()
        db.session.commit()
        return {}, 200
