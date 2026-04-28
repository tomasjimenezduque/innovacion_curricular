import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
# QUITAMOS DeclarativeBase de aquí porque ya está en models/base.py
from models.base import Base 

load_dotenv()

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/innovacion_curricular"

# 2. Motor asíncrono
engine = create_async_engine(
    DATABASE_URL, 
    echo=True, 
    future=True
)

# 3. Fábrica de sesiones
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 4. Dependencia para FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session

# 5. Función para verificar tablas (IMPORTANTE)
async def verificar_tablas():
    """Carga los modelos y crea las tablas si no existen."""
    import models # <--- EL IMPORT VA AQUÍ ADENTRO (Carga diferida)
    try:
        async with engine.begin() as conn:
            # Esto crea las tablas basándose en lo que 'models' registró en 'Base'
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Base de datos verificada: Tablas creadas o ya existentes.")
    except Exception as e:
        print(f"❌ Error al verificar tablas: {e}")

# 6. Prueba de conexión
async def test_connection():
    try:
        async with SessionLocal() as session:
            await session.execute(text("SELECT 1"))
            print("\nCONEXIÓN ASÍNCRONA EXITOSA")
    except Exception as e:
        print(f"\nError detectado en la conexión: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_connection())