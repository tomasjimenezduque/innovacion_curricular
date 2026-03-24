from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import text

# 1. IMPORTANTE: Cambiamos el driver a 'postgresql+asyncpg'
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/innovacion_curricular"

# 2. Creamos el motor asíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# 3. Configuramos la fábrica de sesiones asíncronas
SessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def test_connection():
    try:
        # Usamos 'async with' para la sesión
        async with SessionLocal() as session:
            await session.execute(text("SELECT 1"))
            print("CONEXION ASINCRONA EXITOSA")
    except Exception as e:
        print("Error detectado en la conexion")
        print(str(e))

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_connection())