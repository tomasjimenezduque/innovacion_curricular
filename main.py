from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. Importamos solo los controladores que existen
from controllers.aa_rc_controller import router as aa_rc_router
from controllers.universidad_controller import router as universidad_router

# 2. Instancia de FastAPI
app = FastAPI(
    title="API Innovación Curricular",
    description="Sistema de gestión para Actividades Académicas y Registros Calificados",
    version="1.0.0"
)

# 3. Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Inclusión de Rutas con el prefijo "/api"
# Eliminamos la línea de producto_router para evitar el ModuleNotFoundError
app.include_router(aa_rc_router, prefix="/api", tags=["Actividades"])
app.include_router(universidad_router, prefix="/api", tags=["Universidades"])

# 5. Ruta de bienvenida
@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API de Innovación Curricular",
        "estado": "En línea",
        "documentacion": "/docs"
    }