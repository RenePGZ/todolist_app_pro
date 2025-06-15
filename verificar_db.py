# verificar_db.py

from app import app, db
from sqlalchemy import text

def verificar_tablas():
    print("🔍 Conectando a la base de datos...")
    with app.app_context():
        try:
            with db.engine.connect() as conn:
                resultado = conn.execute(text(
                    "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'"
                ))
                tablas = [row[0] for row in resultado]
                if tablas:
                    print("✅ Tablas encontradas en la base de datos:")
                    for t in tablas:
                        print("   -", t)
                else:
                    print("⚠️  No hay tablas en la base de datos.")
        except Exception as e:
            print("❌ Error al conectar o consultar la base de datos:")
            print(e)

if __name__ == "__main__":
    verificar_tablas()
