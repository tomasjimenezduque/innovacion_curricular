import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text

# Cargamos el archivo .env que está en la raíz de tu proyecto
load_dotenv()

# 1. Configuración de la URL (Driver asyncpg es obligatorio)
# Si prefieres usar variables de entorno, descomenta las líneas de abajo
# DB_USER = os.getenv("DB_USER", "postgres")
# DB_PASS = os.getenv("DB_PASS", "postgres")
# DB_HOST = os.getenv("DB_HOST", "localhost")
# DB_NAME = os.getenv("DB_NAME", "innovacion_curricular")
# DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/innovacion_curricular"

# 2. Motor asíncrono
engine = create_async_engine(
    DATABASE_URL, 
    echo=True, # Muestra el SQL en consola (útil para debugear en Bello)
    future=True
)

# 3. Fábrica de sesiones (Usamos async_sessionmaker)
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 4. Dependencia para FastAPI (La usarás en tus routes)
async def get_db():
    async with SessionLocal() as session:
        yield session

# 5. Prueba de conexión
async def test_connection():
    try:
        async with SessionLocal() as session:
            await session.execute(text("SELECT 1"))
            print("\nCONEXIÓN ASÍNCRONA EXITOSA")
    except Exception as e:
        print("\nError detectado en la conexión:")
        print(f"Detalle: {str(e)}")

if __name__ == "__main__":
    import asyncio
    # Ejecutamos la prueba
    asyncio.run(test_connection())