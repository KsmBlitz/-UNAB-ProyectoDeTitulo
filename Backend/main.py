# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import motor.motor_asyncio
from datetime import datetime

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
MONGO_CONNECTION_STRING = "mongodb+srv://vjestayvaldivia_db_user:KSMblitz3605.@testcluster.fxccig4.mongodb.net/?retryWrites=true&w=majority&appName=TestCluster" 
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONNECTION_STRING)
db = client.SampleDatabase
sensor_collection = db.Sensor_Data


# --- INICIO DE LA APLICACIÓN FASTAPI ---
app = FastAPI()

# Configuración de CORS
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- ENDPOINTS DE LA API ---

@app.get("/")
def read_root():
    return {"status": "Servidor FastAPI conectado a MongoDB Atlas"}

@app.get("/api/metrics/latest")
async def get_latest_metrics():
    """
    Busca el documento más reciente y lo transforma al formato que el frontend necesita,
    ahora incluyendo Nitrógeno y Electroconductividad.
    """
    latest_reading = await sensor_collection.find_one({}, sort=[("ReadTime", -1)])

    if latest_reading:
        # Lógica de transformación actualizada
        transformed_data = {
            "temperatura": { 
                "value": latest_reading.get("Temperature", 0),
                "unit": "C°", 
                "changeText": "Leído desde la DB", 
                "isPositive": True 
            },
            "ph": { 
                "value": latest_reading.get("pH_Value", 0),
                "unit": "",
                "changeText": "Leído desde la DB",
                "isPositive": True 
            },
            
            # --- CAMBIOS AQUÍ ---
            # Reemplazamos "oxigeno_disuelto" por "nitrogeno"
            "nitrogeno": { 
                "value": latest_reading.get("Nitrogen", 0), 
                "unit": "mg/kg", # Unidad común para nitrógeno en suelo
                "changeText": "Nivel en suelo", 
                "isPositive": True 
            },
            # Reemplazamos "salinidad" por "electroconductividad"
            "electroconductividad": { 
                "value": latest_reading.get("EC", 0), 
                "unit": "dS/m", # Unidad común para EC
                "changeText": "Conductividad", 
                "isPositive": True 
            },
        }
        return transformed_data
    else:
        raise HTTPException(status_code=404, detail="No se encontraron lecturas de sensores")