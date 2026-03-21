# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.aa_rc_controller import router as aa_rc_router

# 1. Creamos la instancia de FastAPI
app = FastAPI(
    title="API Innovación Curricular",
    description="Sistema de gestión para Actividades Académicas y Registros Calificados",
    version="1.0.0"
)

# 2. Configuración de CORS (Importante para que el frontend pueda hablar con la API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción usa la URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Incluimos tus rutas (Controllers)
app.include_router(aa_rc_router)

# 4. Ruta de bienvenida (opcional)
@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API de Innovación Curricular",
        "estado": "En línea",
        "documentacion": "/docs"
    }