from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
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
    username: str
    texto: str

# 📂 Función para manejar la conexión a la base de datos
def get_db():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()

# 📂 Inicializar la base de datos y crear tablas si no existen
def init_db():
    conn = sqlite3.connect("database.db", check_same_thread=False)
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
    conn.close()

init_db()

# 🟢 **Registro de Usuario**
@app.post("/register/")
def register(user: UserCreate, db=Depends(get_db)):
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    hashed_password = pwd_context.hash(user.password)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, hashed_password))
    db.commit()
    
    return {"message": "Usuario creado exitosamente"}

# 🔐 **Inicio de Sesión**
@app.post("/login/")
def login(user: UserLogin, db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (user.username,))
    user_data = cursor.fetchone()

    if not user_data or not pwd_context.verify(user.password, user_data[0]):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    return {"message": "Inicio de sesión exitoso"}

# 📊 **Función para analizar sentimiento y guardar en la BD**
def analizar_y_guardar(entrada: TextoEntrada, db):
    resultado = analizar_sentimiento(entrada.texto)
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO historial (username, texto, sentimiento, confianza, fecha) 
        VALUES (?, ?, ?, ?, ?)
    """, (entrada.username, entrada.texto, resultado["sentimiento"], resultado["confianza"], fecha_actual))
    
    db.commit()

# 📊 **Analizar Sentimiento en Segundo Plano**
@app.post("/analizar/")
def analizar_sentimiento_api(entrada: TextoEntrada, background_tasks: BackgroundTasks, db=Depends(get_db)):
    background_tasks.add_task(analizar_y_guardar, entrada, db)
    return {"message": "Análisis en proceso"}

# 🔄 **Obtener Historial de un Usuario**
@app.get("/historial/{username}")
def obtener_historial(username: str, db=Depends(get_db)):
    cursor = db.cursor()
    
    cursor.execute("SELECT texto, sentimiento, confianza, fecha FROM historial WHERE username = ? ORDER BY fecha DESC", (username,))
    historial = cursor.fetchall()

    if not historial:
        return []  # ✅ Devolvemos una lista vacía en lugar de un error

    return [
        {"texto": row[0], "sentimiento": row[1], "confianza": row[2], "fecha": row[3]}
        for row in historial
    ]
