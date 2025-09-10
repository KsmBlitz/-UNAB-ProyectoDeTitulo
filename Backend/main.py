# backend/main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
import motor.motor_asyncio

# --- CARGAR VARIABLES DE ENTORNO ---
load_dotenv() # Carga las variables del archivo .env

# --- CONFIGURACIÓN DE SEGURIDAD ---
SECRET_KEY = "'3vH99@vZN[<Cbh2b_jJ?E4v0'?S8GJJpCKy,e09e@.2m9c_tG"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
# Ahora lee la cadena de conexión desde las variables de entorno
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")

# Verificación para asegurar que la variable de entorno existe
if not MONGO_CONNECTION_STRING:
    raise ValueError("No se encontró la variable de entorno MONGO_CONNECTION_STRING. Asegúrate de crear un archivo .env.")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONNECTION_STRING)
db = client.SampleDatabase
users_collection = db.users
sensor_collection = db.Sensor_Data

# --- MODELOS (PYDANTIC) ---
# ... (Los modelos User, UserInDB, Token se mantienen igual) ...
class User(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# --- FUNCIONES DE UTILIDAD DE AUTENTICACIÓN ---
# ... (verify_password y create_access_token se mantienen igual) ...
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- INICIO DE LA APLICACIÓN FASTAPI ---
app = FastAPI()

# Configuración de CORS
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


# --- ENDPOINTS ---
# ... (Todos los endpoints se mantienen exactamente igual) ...
@app.get("/")
def read_root():
    return {"status": "Servidor FastAPI conectado y con autenticación"}

@app.post("/api/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/metrics/latest")
async def get_latest_metrics():
    latest_reading = await sensor_collection.find_one({}, sort=[("ReadTime", -1)])
    if latest_reading:
        transformed_data = {
            "temperatura": {"value": latest_reading.get("Temperature", 0), "unit": "C°", "changeText": "Leído desde la DB", "isPositive": True},
            "ph": {"value": latest_reading.get("pH_Value", 0), "unit": "", "changeText": "Leído desde la DB", "isPositive": True},
            "nitrogeno": {"value": latest_reading.get("Nitrogen", 0), "unit": "mg/kg", "changeText": "Nivel en suelo", "isPositive": True},
            "electroconductividad": {"value": latest_reading.get("EC", 0), "unit": "dS/m", "changeText": "Conductividad", "isPositive": True},
        }
        return transformed_data
    else:
        raise HTTPException(status_code=404, detail="No se encontraron lecturas de sensores")