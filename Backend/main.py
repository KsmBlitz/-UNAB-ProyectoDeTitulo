# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. Crear una instancia de FastAPI
app = FastAPI()

# 2. Configurar CORS (MUY IMPORTANTE)
# Esto permite que tu frontend (ej. en localhost:5173) pueda hacer peticiones a tu backend (en localhost:8000)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Definir un endpoint (una "ruta") para las métricas
@app.get("/api/metrics/latest")
def get_latest_metrics():
    """
    Este endpoint devuelve los valores más recientes de las métricas principales.
    Por ahora, son datos de ejemplo. En el futuro, los leeremos de MongoDB.
    """
    return {
        "temperatura": { "value": 14.2, "unit": "C°", "changeText": "-2.2 C° bajo lo esperado", "isPositive": True },
        "oxigeno_disuelto": { "value": 0.25, "unit": "PPM", "changeText": "-$2,201", "isPositive": False },
        "salinidad": { "value": 45, "unit": "", "changeText": "+5.39 sobre lo esperado", "isPositive": False },
        "ph": { "value": 7.0, "unit": "", "changeText": "-1.22 bajo lo esperado", "isPositive": True },
    }

# Endpoint raíz para verificar que el servidor funciona
@app.get("/")
def read_root():
    return {"status": "El servidor FastAPI está funcionando"}