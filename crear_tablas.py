# crear_tablas.py

from app import app, db

def crear_tablas():
    with app.app_context():
        try:
            db.create_all()
            print("✅ Tablas creadas exitosamente en la base de datos PostgreSQL.")
        except Exception as e:
            print("❌ Error al crear las tablas:", e)

if __name__ == "__main__":
    crear_tablas()
