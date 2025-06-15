# ver_tablas.py

from app import app, db
from sqlalchemy import text

def mostrar_tablas():
    print("🔎 Verificando tablas en la base de datos PostgreSQL...\n")
    with app.app_context():
        try:
            with db.engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public'"
                ))
                tablas = [row[0] for row in result]
                if tablas:
                    print("✅ Tablas encontradas:")
                    for tabla in tablas:
                        print("   -", tabla)
                else:
                    print("⚠️  No se encontró ninguna tabla en la base de datos.")
        except Exception as e:
            print("❌ Error al consultar las tablas:", e)

if __name__ == "__main__":
    mostrar_tablas()
