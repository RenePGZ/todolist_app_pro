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
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # 🧠 Base en memoria
    app.config["WTF_CSRF_ENABLED"] = False

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()

            # Solo inserta si no existe (aunque en memoria no debería existir)
            user = User(
                username="testuser",
                email="test@example.com",
                password=generate_password_hash("test123")
            )
            db.session.add(user)
            db.session.commit()

        yield client
