# reset_db.py
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

# Conexión como superusuario dentro de Codespaces
engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
conn = engine.connect()
conn.execution_options(isolation_level="AUTOCOMMIT")

# Eliminar base de datos si existe
try:
    conn.execute("DROP DATABASE IF EXISTS mjsosphia;")
    print("Base de datos eliminada")
except ProgrammingError as e:
    print(f"Error al eliminar DB: {e}")

# Crear base de datos nueva
try:
    conn.execute("CREATE DATABASE MJSOSPHIA;")
    print("Base de datos creada")
except ProgrammingError as e:
    print(f"Error al crear DB: {e}")

conn.close()
