from app import app
import logging
from dotenv import load_dotenv

load_dotenv()  # Solo útil en local, no afecta Render

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

if __name__ == "__main__":
    app.run(debug=True)
