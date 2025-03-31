import sqlite3

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect("sentiment_analysis.db")
cursor = conn.cursor()

# Crear tabla de usuarios
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Crear tabla de análisis de sentimientos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS analisis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        texto TEXT NOT NULL,
        sentimiento TEXT NOT NULL,
        confianza REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES usuarios(id)
    )
''')

conn.commit()
conn.close()

print("Base de datos inicializada correctamente.")
