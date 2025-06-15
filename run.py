from app import app
import logging
import os
from dotenv import load_dotenv

load_dotenv()  # Carga variables de .env

# Configura Flask
app.secret_key = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

if __name__ == "__main__":
    app.run(debug=True)
