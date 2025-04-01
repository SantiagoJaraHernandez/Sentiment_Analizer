from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from passlib.context import CryptContext
from datetime import datetime
from sentiment_analysis import analizar_sentimiento

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 📌 Modelos de datos
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TextoEntrada(BaseModel):
    username: str  # Ahora pedimos el usuario para guardar su análisis
    texto: str

# 📂 Inicializar la base de datos y crear tablas si no existen
def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                texto TEXT NOT NULL,
                sentimiento TEXT NOT NULL,
                confianza REAL NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()

init_db()

# 🟢 **Registro de Usuario**
@app.post("/register/")
def register(user: UserCreate):
    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()

            # Verificar si el usuario ya existe
            cursor.execute("SELECT id FROM users WHERE username = ?", (user.username,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="El usuario ya existe")

            hashed_password = pwd_context.hash(user.password)
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, hashed_password))
            conn.commit()

        return {"message": "Usuario creado exitosamente"}
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")

# 🔐 **Inicio de Sesión**
@app.post("/login/")
def login(user: UserLogin):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE username = ?", (user.username,))
        user_data = cursor.fetchone()

        if not user_data or not pwd_context.verify(user.password, user_data[0]):
            raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    return {"message": "Inicio de sesión exitoso"}

# 📊 **Analizar Sentimiento y Guardarlo en Historial**
@app.post("/analizar/")
def analizar_sentimiento_api(entrada: TextoEntrada):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()

        # 🔍 Verificar si el usuario existe antes de procesar la solicitud
        cursor.execute("SELECT id FROM users WHERE username = ?", (entrada.username,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="El usuario no existe")

        # Obtener resultado del análisis
        resultado = analizar_sentimiento(entrada.texto)

        # Guardar en la base de datos
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO historial (username, texto, sentimiento, confianza, fecha) 
            VALUES (?, ?, ?, ?, ?)
        """, (entrada.username, entrada.texto, resultado["sentimiento"], resultado["confianza"], fecha_actual))
        
        conn.commit()

    return resultado

# 🔄 **Obtener Historial de un Usuario**
@app.get("/historial/{username}")
def obtener_historial(username: str):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()

        # Verificar si el usuario existe
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="El usuario no existe")

        cursor.execute("SELECT texto, sentimiento, confianza, fecha FROM historial WHERE username = ? ORDER BY fecha DESC", (username,))
        historial = cursor.fetchall()

    if not historial:
        return []  # ✅ Devolvemos una lista vacía en lugar de un mensaje de error

    return [
        {
            "texto": row[0], 
            "sentimiento": row[1], 
            "confianza": round(row[2], 2),  # Redondear confianza
            "fecha": datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y %H:%M")  # Formato de fecha más legible
        }
        for row in historial
    ]
