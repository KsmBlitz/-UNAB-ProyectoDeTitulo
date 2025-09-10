# backend/main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
import motor.motor_asyncio
from bson import ObjectId

# --- CARGAR VARIABLES DE ENTORNO ---
load_dotenv()

# --- CONFIGURACIÓN DE SEGURIDAD ---
SECRET_KEY = "'3vH99@vZN[<Cbh2b_jJ?E4v0'?S8GJJpCKy,e09e@.2m9c_tG"
ALGORITHM = "HS256"  # <-- ¡AQUÍ ESTÁ LA CORRECCIÓN!
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
if not MONGO_CONNECTION_STRING:
    raise ValueError("No se encontró la variable MONGO_CONNECTION_STRING.")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONNECTION_STRING)
db = client.SampleDatabase
users_collection = db.users
sensor_collection = db.Sensor_Data

# --- MODELOS (PYDANTIC) ---
class TokenData(BaseModel):
    email: Optional[str] = None

class User(BaseModel):
    id: str = Field(alias='_id')
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    disabled: Optional[bool] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# --- FUNCIONES DE UTILIDAD DE AUTENTICACIÓN ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- DEPENDENCIAS DE SEGURIDAD ---
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await users_collection.find_one({"email": token_data.email})
    if user is None:
        raise credentials_exception
    return user

async def get_current_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes. Se requiere rol de administrador."
        )
    return current_user

# --- INICIO DE LA APLICACIÓN FASTAPI ---
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- ENDPOINTS ---
@app.get("/")
def read_root():
    return {"status": "Servidor FastAPI conectado y con autenticación"}

@app.post("/api/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Correo o contraseña incorrectos")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "role": user.get("role", "operario")},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/metrics/latest")
async def get_latest_metrics(current_user: dict = Depends(get_current_user)):
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

@app.get("/api/users", response_model=List[User])
async def read_users(admin_user: dict = Depends(get_current_admin_user)):
    users_cursor = users_collection.find()
    users = []
    async for user in users_cursor:
        user['_id'] = str(user['_id'])
        users.append(user)
    return users