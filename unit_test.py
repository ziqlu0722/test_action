from app import create_app, db
from config import TestConfig
from app.models import User
import pytest
import base64
from datetime import datetime

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(TestConfig)
 
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
 
    yield testing_client  # this is where the testing happens!
 
    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()
 
    # Insert user data
    u1 = User(email_address='kate@example.com', first_name='kate', last_name='Li')
    u1.set_password('password123!')
    u1.account_created = datetime.utcnow()

    u2 = User(email_address='zoe@example.com', first_name='zoe', last_name='Li')
    u2.set_password('password123!')
    u2.account_created = datetime.utcnow()

    db.session.add(u1)
    db.session.add(u2)
 
    # Commit the changes for the users
    db.session.commit()
 
    yield db  # this is where the testing happens!
    db.session.remove()
    db.drop_all()

def test_duplicate_email(test_client, init_database):
    # GIVEN  user A is registered and user B is not registered
    # WHEN   user B uses a same email_address to register as user A
    # THEN   registration fails
    
    u3_payload = { 
                    "email_address": "kate@example.com", 
                    "first_name": "kate", 
                    "last_name": "Li", 
                    "password": "password123!"
                 }

    # json as name of the second argument
    response = test_client.post('/v1/user',
                                json=u3_payload)

    assert response.status_code==400
    assert b'already exists' in response.data

def test_successful_register(test_client, init_database):
    # GIVEN  user A is not registered
    # WHEN   user A register using the correct payload
    # THEN   registration succeeds
    
    u4_payload = { 
                    "email_address": "ann@example.com", 
                    "first_name": "ann", 
                    "last_name": "Li", 
                    "password": "password123!"
                 }

    # json as name of the second argument
    response = test_client.post('/v1/user',
                                json=u4_payload)

    assert response.status_code==201

def test_successful_login(test_client, init_database):
    # GIVEN  user A is registered
    # WHEN   user A log-in via basic-auth
    # THEN   log-in succeeds
    credential = base64.b64encode(b"kate@example.com:password123!").decode('utf-8')
    headers = {'Authorization': 'Basic {}'.format(credential)}

    response = test_client.get('/v1/user/self',
                                headers=headers)

    assert response.status_code==200

def test_update_created(test_client, init_database):
    # GIVEN  user A is registered
    # WHEN   user A update account_created data
    # THEN   update fails
    credential = base64.b64encode(b"kate@example.com:password123!").decode('utf-8')
    headers = {'Authorization': 'Basic {}'.format(credential)}
    update_payload = {"account_created": datetime.utcnow()}

    response = test_client.put('/v1/user/self',
                               json=update_payload,
                               headers=headers)

    assert response.status_code==400
    assert b'cannot be updated' in response.data

def test_update_password(test_client, init_database):
    # GIVEN  user A is registered
    # WHEN   user A update password data
    # THEN   update succeeds
    credential = base64.b64encode(b"kate@example.com:password123!").decode('utf-8')
    headers = {'Authorization': 'Basic {}'.format(credential)}
    update_payload = {"password": 'password123@'}

    response = test_client.put('/v1/user/self',
                               json=update_payload,
                               headers=headers)

    assert response.status_code==204