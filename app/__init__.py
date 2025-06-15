import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()

# Crear la app
app = Flask(__name__)

# Configurar desde variables de entorno
app.secret_key = os.environ.get("SECRET_KEY", "clave-temporal-dev")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar extensiones
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

from app import routes, models
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import error_handlers
