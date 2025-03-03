import csv
import pytest
from app import app, load_users_from_csv, USERS
from flask import url_for
from models.user import User

# A dummy to use in tests
class DummyUser:
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

@pytest.fixture
def client():
    app.config['TESTING'] = True
    USERS.clear()
    dummy = DummyUser('1', 'testuser')
    USERS['testuser'] = dummy

    with app.test_client() as client:
        yield client

def login(client):
    # Set the session to simulate a logged in user
    with client.session_transaction() as sess:
        sess['_user_id'] = '1'

def test_dashboard_unauthorized(client):
    # Without logging in, should redirect (302)
    resp = client.get('/dashboard')
    assert resp.status_code == 302

def test_dashboard_authorized(client):
    login(client)
    resp = client.get('/dashboard')
    assert resp.status_code == 200
    # You could further check that rendered HTML contains expected content,
    # e.g. "dashboard" in some form.
    assert b"dashboard" in resp.data.lower()

def test_reports_authorized(client):
    login(client)
    resp = client.get('/reports')
    assert resp.status_code == 200

def test_orders_json_response(client):
    login(client)
    # Request with Accept header for JSON (or a User-Agent containing "curl")
    resp = client.get('/orders', headers={
        "Accept": "application/json",
        "User-Agent": "python-requests"
    })
    assert resp.status_code == 401
    json_data = resp.get_json()
    assert "error" in json_data

def test_orders_html_response(client):
    login(client)
    # With a normal User-Agent, expecting HTML response
    resp = client.get('/orders', headers={"User-Agent": "Mozilla/5.0"})
    assert resp.status_code == 200

def test_products_authorized(client):
    login(client)
    resp = client.get('/products')
    assert resp.status_code == 200

def test_user_management_authorized(client):
    login(client)
    resp = client.get('/user-management')
    assert resp.status_code == 200

def test_settings_authorized(client):
    login(client)
    resp = client.get('/settings')
    assert resp.status_code == 200

def test_load_users_from_csv(tmp_path):
    # Create a temporary CSV file with user data
    csv_file = tmp_path / "users.csv"
    header = "id,username,password,role\n"
    row = "1,testcsv,dummypass,admin\n"
    csv_file.write_text(header + row)

    users = load_users_from_csv(str(csv_file))
    assert "testcsv" in users
    # user = User(users["testcsv"])
    user = users["testcsv"]
    # Ensure that the dummy user loaded from CSV returns the correct id
    assert user.get_id() == "1"
