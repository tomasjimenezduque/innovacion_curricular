from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from database.connection import engine, Base 
import models

# 1. Importamos los controladores
from controllers.aa_rc_controller import router as aa_rc_router
from controllers.universidad_controller import router as universidad_router
from controllers.facultad_controller import router as facultad_router
from controllers.programa_controller import router as programa_router
from controllers.usuario_controller import router as usuario_router
from controllers.rol_controller import router as rol_router
from controllers.aliado_controller import router as aliado_router
from controllers.acreditacion_controller import router as acreditacion_router
from controllers.pasantia_controller import router as pasantia_router
from controllers.registro_calificado_controller import router as registro_router
from controllers.premio_controller import router as premio_router
from controllers.enfoque_controller import router as enfoque_router
from controllers.alianza_controller import router as alianza_router
from controllers.practica_estrategia_controller import router as practica_router
from controllers.car_innovacion_controller import router as car_innovacion_router
from controllers.aspecto_normativo_controller import router as aspecto_router
from controllers.asociaciones_controller import router as asociaciones_router
from controllers.area_conocimiento_controller import router as area_router
from controllers.activ_academica_controller import router as activ_academica_router
from controllers.docente_departamento_controller import router as docente_router

# 2. Instancia de FastAPI
app = FastAPI(
    title="API Innovación Curricular",
    description="Sistema de gestión para Actividades Académicas y Registros Calificados",
    version="1.0.0"
)

# --- 2.1 LÓGICA PARA CREAR TABLAS AL INICIAR ---
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # Esto buscará todos los modelos (incluyendo Aliado) y creará las tablas si no existen
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Base de datos verificada: Tablas creadas o ya existentes.")

# 3. Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Inclusión de Rutas (Prefijo /api)
app.include_router(universidad_router, prefix="/api", tags=["Universidades"])
app.include_router(facultad_router, prefix="/api", tags=["Facultades"])
app.include_router(programa_router, prefix="/api", tags=["Programas"])
app.include_router(usuario_router, prefix="/api", tags=["Usuarios"])
app.include_router(rol_router, prefix="/api", tags=["Roles"])
app.include_router(acreditacion_router, prefix="/api", tags=["Acreditaciones"])
app.include_router(registro_router, prefix="/api", tags=["Registros Calificados"])
app.include_router(enfoque_router, prefix="/api", tags=["Enfoques Pedagógicos"])
app.include_router(area_router, prefix="/api", tags=["Áreas de Conocimiento"])
app.include_router(aliado_router, prefix="/api", tags=["Aliados"])
app.include_router(alianza_router, prefix="/api", tags=["Alianzas"])
app.include_router(pasantia_router, prefix="/api", tags=["Pasantías"])
app.include_router(car_innovacion_router, prefix="/api", tags=["Características Innovación"])
app.include_router(practica_router, prefix="/api", tags=["Prácticas y Estrategias"])
app.include_router(premio_router, prefix="/api", tags=["Premios"])
app.include_router(aspecto_router, prefix="/api", tags=["Aspectos Normativos"])
app.include_router(asociaciones_router, prefix="/api", tags=["Asociaciones"])
app.include_router(activ_academica_router, prefix="/api", tags=["Actividades Académicas"])
app.include_router(docente_router, prefix="/api", tags=["Docentes Departamentos"])
app.include_router(aa_rc_router, prefix="/api", tags=["Relación AA-RC"])

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API de Innovación Curricular",
        "estado": "En línea",
        "documentacion": "/docs"
    }