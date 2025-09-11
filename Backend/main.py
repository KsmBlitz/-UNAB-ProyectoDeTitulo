# backend/main.py

# 1. Imports
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pydantic_settings import BaseSettings
from typing import Annotated, Optional, List
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
import motor.motor_asyncio
from bson import ObjectId

# Importar core_schema y PydanticCustomError para PyObjectId
from pydantic_core import CoreSchema, PydanticCustomError, core_schema


# --------------------------------------------------------------------------
# 2. Configuración Centralizada (Lee desde el archivo .env)
# --------------------------------------------------------------------------
class Settings(BaseSettings):
    MONGO_CONNECTION_STRING: str
    DATABASE_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()

# --------------------------------------------------------------------------
# 3. Conexión a la Base de Datos
# --------------------------------------------------------------------------
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
db = client[settings.DATABASE_NAME]
users_collection = db.users
sensor_collection = db.Sensor_Data

# --------------------------------------------------------------------------
# 4. Modelos de Datos (Pydantic) - CON LA CORRECCIÓN FINAL PARA ObjectId
# --------------------------------------------------------------------------

# Clase PyObjectId personalizada para Pydantic v2
# Esta es la implementación recomendada para manejar ObjectId en Pydantic v2
# Tomado de la documentación de Pydantic/FastAPI
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: any, handler) -> CoreSchema:
        def validate_from_str(input_value: str) -> ObjectId:
            if not ObjectId.is_valid(input_value):
                raise PydanticCustomError("object_id", "Invalid ObjectId")
            return ObjectId(input_value)

        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(), # Cuando se envía a JSON, es un string
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId), # Si ya es ObjectId, lo acepta
                core_schema.no_info_after_validator_function(validate_from_str, core_schema.str_schema()) # Si es string, lo valida y convierte a ObjectId
            ]),
            serialization=core_schema.to_string_ser_schema(), # Cómo serializar de ObjectId a string
        )

# Para usar este tipo personalizado en los modelos
# No necesitamos Annotated con BeforeValidator si PyObjectId ya define el schema
# Solo necesitamos importarlo de typing
from typing import Any # Asegúrate de que Any esté importado


class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    disabled: Optional[bool] = False

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    disabled: Optional[bool] = None

class UserPublic(UserBase):
    id: PyObjectId = Field(alias='_id') # Usamos el tipo PyObjectId
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True, # Permitir que PyObjectId sea un tipo arbitrario
        json_encoders={ObjectId: str} # Asegurarse de que ObjectId se convierta a str en la salida JSON
    )

class UserCreate(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# --------------------------------------------------------------------------
# 5. Utilidades y Dependencias de Seguridad (sin cambios)
# --------------------------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No se pudieron validar las credenciales", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None: raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await users_collection.find_one({"email": email})
    if user is None: raise credentials_exception
    return user

async def get_current_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permisos de administrador requeridos")
    return current_user
# --------------------------------------------------------------------------
# 6. Inicialización de la App FastAPI
# --------------------------------------------------------------------------
app = FastAPI(title="API para Dashboard de Embalses IoT", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --------------------------------------------------------------------------
# 7. Endpoints de la API
# --------------------------------------------------------------------------
@app.get("/", tags=["Root"])
def read_root():
    return {"status": "Servidor FastAPI conectado y con autenticación"}

@app.post("/api/token", response_model=Token, tags=["Autenticación"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Correo o contraseña incorrectos")
    access_token = create_access_token(
        data={"sub": user["email"], "role": user.get("role"), "full_name": user.get("full_name")}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users", response_model=List[UserPublic], tags=["Usuarios"])
async def read_users(admin_user: dict = Depends(get_current_admin_user)):
    users_from_db = await users_collection.find().to_list(1000) # Increased limit
    # Pydantic con PyObjectId ahora manejará la conversión de ObjectId a str automáticamente
    return [UserPublic(**user) for user in users_from_db]

@app.post("/api/users", response_model=UserPublic, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
async def create_user(user: UserCreate, admin_user: dict = Depends(get_current_admin_user)):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user: raise HTTPException(status_code=400, detail="Ya existe un usuario con este email")
    hashed_password = get_password_hash(user.password)
    user_data = user.model_dump(exclude={"password"})
    user_data["hashed_password"] = hashed_password
    new_user_doc = await users_collection.insert_one(user_data)
    created_user_from_db = await users_collection.find_one({"_id": new_user_doc.inserted_id})
    return UserPublic(**created_user_from_db)

@app.put("/api/users/{user_id}", response_model=UserPublic, tags=["Usuarios"])
async def update_user(user_id: str, user_update: UserUpdate, admin_user: dict = Depends(get_current_admin_user)):
    if not ObjectId.is_valid(user_id): raise HTTPException(status_code=400, detail="El ID de usuario no es válido")
    update_data = {k: v for k, v in user_update.model_dump().items() if v is not None}
    if not update_data: raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")
    
    result = await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    if result.matched_count == 0: raise HTTPException(status_code=404, detail="No se encontró el usuario")
    
    updated_user_from_db = await users_collection.find_one({"_id": ObjectId(user_id)})
    return UserPublic(**updated_user_from_db)

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Usuarios"])
async def delete_user(user_id: str, admin_user: dict = Depends(get_current_admin_user)):
    if not ObjectId.is_valid(user_id): raise HTTPException(status_code=400, detail="El ID de usuario no es válido")
    if str(admin_user["_id"]) == user_id: raise HTTPException(status_code=403, detail="Un administrador no puede eliminarse a sí mismo")
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0: raise HTTPException(status_code=404, detail="No se encontró el usuario a eliminar")
    return

@app.get("/api/metrics/latest", tags=["Datos de Sensores"])
async def get_latest_metrics(current_user: dict = Depends(get_current_user)):
    latest_reading = await sensor_collection.find_one({}, sort=[("ReadTime", -1)])
    if not latest_reading: raise HTTPException(status_code=404, detail="No se encontraron lecturas de sensores")
    return {
        "temperatura": {"value": latest_reading.get("Temperature", 0), "unit": "C°", "changeText": "Leído desde la DB", "isPositive": True},
        "ph": {"value": latest_reading.get("pH_Value", 0), "unit": "", "changeText": "Leído desde la DB", "isPositive": True},
        "nitrogeno": {"value": latest_reading.get("Nitrogen", 0), "unit": "mg/kg", "changeText": "Nivel en suelo", "isPositive": True},
        "electroconductividad": {"value": latest_reading.get("EC", 0), "unit": "dS/m", "changeText": "Conductividad", "isPositive": True},
    }

@app.get("/api/charts/water-level", tags=["Datos de Sensores"])
async def get_water_level_data(
    current_user: dict = Depends(get_current_user),
    start_date: Optional[datetime] = None, # Nuevo parámetro: fecha de inicio
    end_date: Optional[datetime] = None,   # Nuevo parámetro: fecha de fin
    limit: int = 30 # Por si queremos limitar el número de puntos
):
    query = {}
    if start_date:
        query["ReadTime"] = {"$gte": start_date}
    if end_date:
        if "ReadTime" in query:
            query["ReadTime"]["$lte"] = end_date
        else:
            query["ReadTime"] = {"$lte": end_date}
            
    # Siempre ordenar por ReadTime ascendente para el gráfico
    cursor = sensor_collection.find(query).sort("ReadTime", 1) 
    
    # Si hay un límite y no estamos filtrando por rango de fecha, aplicarlo
    # Si tenemos un rango de fecha, queremos todos los datos de ese rango
    if not start_date and not end_date:
        cursor = cursor.limit(limit)

    readings = await cursor.to_list(length=None) # Obtenemos todos los resultados de la consulta
    
    if not readings:
        raise HTTPException(status_code=404, detail="No hay datos disponibles para el rango seleccionado")

    # Determinar el formato de la etiqueta basado en el rango de fechas
    # Si el rango es de un día o menos, mostrar fecha y hora
    # Si es más largo, solo mostrar fecha
    
    # Calcular el rango real de los datos obtenidos
    first_time = readings[0]["ReadTime"]
    last_time = readings[-1]["ReadTime"]
    data_range = last_time - first_time

    if data_range < timedelta(days=2): # Menos de 48 horas, mostrar fecha y hora
        time_format = "%d-%m %H:%M" # Día-Mes Hora:Minuto
    else: # Más de un día, solo mostrar fecha
        time_format = "%d-%m" # Día-Mes

    return {
        "labels": [r["ReadTime"].strftime(time_format) for r in readings],
        "real_level": [r.get("Potassium", 0) for r in readings], # Asumiendo Potassium como "nivel de agua"
        "expected_level": [r.get("Potassium", 0) + 5 for r in readings] # Nivel esperado
    }