import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Crear tabla de usuarios si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ Base de datos inicializada correctamente.")
