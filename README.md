# Dashboard IoT para Monitoreo de Embalses

![Vue.js](https://img.shields.io/badge/Vue.js-3-4FC08D?logo=vue.js)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb)
![MQTT](https://img.shields.io/badge/MQTT-660066?logo=mqtt)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker)

Sistema de monitoreo IoT full-stack diseñado para la agricultura de precisión. Este proyecto provee una solución completa para la recolección, almacenamiento, procesamiento y visualización de datos de sensores ubicados en embalses de agua para cultivos de arándanos.

El objetivo es ofrecer una herramienta centralizada que permita a los operarios tomar decisiones basadas en datos para optimizar el uso de recursos hídricos, predecir tendencias y actuar de forma proactiva ante posibles problemas.

---

## 🖼️ Vista Previa del Dashboard

![Captura del Dashboard](URL_DE_TU_MEJOR_IMAGEN.png)

---

## 🏗️ Diagrama de Arquitectura

El sistema está compuesto por varios servicios que se comunican entre sí, orquestados por Docker para un despliegue simplificado.

<img width="1048" height="953" alt="image" src="https://github.com/user-attachments/assets/1a876814-8bb4-4074-bcfa-0d846f5fbc25" />


## ✨ Características Principales

* **Frontend Interactivo:** Un dashboard moderno construido con Vue 3 y TypeScript.
* **Visualización de Datos:** Gráficos y tablas en tiempo real con Chart.js para un fácil entendimiento de los datos.
* **Backend de Alto Rendimiento:** Una API RESTful construida con FastAPI (Python) que maneja la lógica de negocio.
* **Comunicación en Tiempo Real:** Suscripción a un Broker MQTT para la ingesta instantánea de datos desde los sensores.
* **Almacenamiento Persistente:** Uso de MongoDB, una base de datos NoSQL ideal para datos de series temporales de IoT.
* **Inteligencia Artificial:** Integración de un modelo de Machine Learning (SVM/XGBoost) para realizar predicciones.
* **Containerización:** Todo el sistema (frontend, backend, DB, broker) está dockerizado para un despliegue y desarrollo consistentes.

---

## 🛠️ Tecnologías Utilizadas

| Área                 | Tecnología                                               |
| -------------------- | -------------------------------------------------------- |
| **Frontend** | Vue 3 (Composition API), TypeScript, Vite, Chart.js      |
| **Backend** | Python 3, FastAPI, Pydantic, Uvicorn                     |
| **Base de Datos** | MongoDB                                                  |
| **Comunicación IoT** | MQTT (Broker como Mosquitto/VerneMQ)                     |
| **Machine Learning** | Scikit-learn (SVM) o XGBoost                             |
| **DevOps** | Docker, Docker Compose                                   |
| **Calidad de Código** | ESLint, Prettier                                         |

---

## 🚀 Instalación y Puesta en Marcha

### Con Docker (Método Recomendado)

Este método levantará todos los servicios necesarios con un solo comando.

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
    cd tu-repositorio
    ```
2.  **Construye y levanta los contenedores:**
    ```bash
    docker-compose up --build
    ```
    * El Frontend estará disponible en `http://localhost:5173`.
    * El Backend estará disponible en `http://localhost:8000`.

### Manualmente (Para Desarrollo)

Si prefieres ejecutar cada servicio por separado:

1.  **Backend (FastAPI):**
    ```bash
    cd backend
    pip install -r requirements.txt
    uvicorn main:app --reload
    ```
2.  **Frontend (Vue):**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

---

## 📁 Estructura Sugerida del Repositorio

/
├── backend/          # Código del servicio FastAPI
├── frontend/         # Código de la aplicación Vue.js
├── docker-compose.yml # Archivo de orquestación de Docker
└── README.md         # Este archivo


---

## 📝 Trabajo a Futuro

* [ ] Implementar y entrenar el modelo de predicción (SVM/XGBoost).
* [ ] Desarrollar los endpoints de la API en FastAPI.
* [ ] Conectar el frontend con la API real en lugar de usar datos de ejemplo.
* [ ] Crear el script de Python que se suscribe al broker MQTT y guarda en MongoDB.
* [ ] Finalizar y pulir el diseño responsivo del frontend.
* [ ] Implementar un sistema de autenticación de usuarios.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
