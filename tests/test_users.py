import pytest

from main import app


@pytest.fixture(scope='module')
def test_client():
    flask_app = app

    # Flask provides a way to test your application by exposing
    # the Werkzeug test Client and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


def test_users_get(test_client):
    response = test_client.get('/users')
    assert response.status_code == 200
    assert b"username" in response.data
    assert b"email" in response.data
    assert b"id" in response.data
    assert {
               "id": 1,
               "username": "Davidka",
               "email": "dave@gmail.com"
           } in response.json


def test_single_user_get(test_client):
    response = test_client.get('/users/1')
    assert response.status_code == 200
    assert b"username" in response.data
    assert b"email" in response.data
    assert b"id" in response.data

    response = test_client.get('/users/1000')
    assert response.status_code == 404
    assert b"Not found" in response.data


def test_single_user_patch(test_client):
    response = test_client.patch('/users/4', json={"username": "Alla"})
    assert response.status_code == 204

    # patching existing user
    response = test_client.patch('/users/2', json={"username": "Davidka"})
    assert response.status_code == 409
    assert b"Either data already exists or wrong input"


def test_single_user_delete(test_client):
    # creating a user
    response = test_client.post('/users', json={"username": "Mark",
                                                "email": "mark@gmail.com"})
    # deleting new user
    user_id = response.json.get("id")
    response = test_client.delete(f'/users/{user_id}')
    assert response.status_code == 200


def test_users_post(test_client):
    # sending empty body
    response = test_client.post('/users')
    assert response.status_code == 400
    assert b"Wrong input" in response.data

    # adding existing user
    response = test_client.post('/users', json={"username": "Davidka",
                                                "email": "dave@gmail.com"})
    assert response.status_code == 409
    assert b"Either data already exists or wrong input"

    # sending wrong data
    response = test_client.post('/users', json={"ddddd": "Davidka"})
    assert response.status_code == 400
    assert b"Wrong input" in response.data




# from models import User, db

# @pytest.fixture(scope='module')
# def new_user():
#     user = User(username='Steve', email='steve@gmail.com')
#     return user
#
#
# def test_new_user(new_user):
#     assert new_user.username == 'Steve'
#     assert new_user.email == 'steve@gmail.com'
#
#
# @pytest.fixture(scope='module')
# def init_database():
#     db.create_all()
#
#     user1 = User(username='Steve', email='steve@gmail.com')
#     user2 = User(username='John', email='john@gmail.com')
#     db.session.add(user1)
#     db.session.add(user2)
#
#     db.session.commit()
#
#     yield db
#
#     db.drop_all()
#

