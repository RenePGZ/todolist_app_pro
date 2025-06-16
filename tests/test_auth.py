import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # DB en RAM
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            user = User(username="testuser", email="test@example.com",
                        password=generate_password_hash("test123"))
            db.session.add(user)
            db.session.commit()
        yield client

def test_login_success(client):
    response = client.post("/login", data={
        "email": "test@example.com",
        "password": "test123"
    }, follow_redirects=True)
    assert "Inicio de sesión exitoso" in response.data.decode()

def test_login_fail(client):
    response = client.post("/login", data={
        "email": "test@example.com",
        "password": "wrongpass"
    }, follow_redirects=True)
    assert "Correo o contraseña incorrectos" in response.data.decode()
