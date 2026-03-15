from sqlmodel import create_engine, Session, text

# USA ESTA URL SIMPLE (Asegúrate de que el nombre sea exacto al de pgAdmin)
# Si tu BD en pgAdmin se llama 'innovacion_curricular', ponlo así:
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/innovacion_curricular"

engine = create_engine(DATABASE_URL)

def test_connection():
    try:
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
            # Usamos un mensaje sin tildes ni emojis para evitar el WinError 6
            print("CONEXION EXITOSA")
    except Exception as e:
        # Imprimimos el error de forma simple
        print("Error detectado")
        print(str(e))

if __name__ == "__main__":
    test_connection()