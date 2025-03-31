from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
import sqlite3
from passlib.context import CryptContext

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_context.hash(password)

def authenticate_user(username: str, password: str):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM usuarios WHERE username = ?", (username,)).fetchone()
    conn.close()
    if user and verify_password(password, user["password"]):
        return user
    return None

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user["username"]}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
