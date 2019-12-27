from sqlalchemy.exc import InvalidRequestError, IntegrityError, StatementError
from sqlalchemy.orm.exc import FlushError
from models import serialize_multiple, User
from settings import db


class ModelValidator:

    def __init__(self, model):
        self.model = model

    def get_by_id(self, model_id):
        try:
            return self.model.query.get(model_id).serialize()
        except AttributeError:
            return "Not found", 404

    def patch_by_id(self, model_id, data):
        try:
            db.session.query(self.model).filter_by(id=model_id).update(data)
        except InvalidRequestError:
            return {}, 400
        except IntegrityError:
            return "Either data already exists or wrong input", 409
        db.session.commit()

        return {}, 204

    def post(self, data):
        try:
            model = self.model(**data)
            db.session.add(model)
            db.session.flush()

            model_id = model.id
            db.session.commit()

            return {"id": model_id}, 201

        except TypeError:
            return "Wrong input", 400

        except IntegrityError:
            return "Either data already exists or wrong input", 409

        except StatementError:
            return "You can't manipulate creation time"

    def get_model_in_room_by_id(self, model_id):
        try:
            return serialize_multiple(self.model.query.get(model_id).users)
        except AttributeError:
            return "Not found", 404

    def post_model_in_room_by_id(self, model_id, user_id):
        try:
            model = self.model.query.get(model_id)
            model.users.append(User.query.get(user_id))

            db.session.commit()

            return {}, 201

        except AttributeError:
            return "Not found", 404

        except FlushError:
            return "Wrong input", 404
