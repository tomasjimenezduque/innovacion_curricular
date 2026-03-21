from sqlalchemy.orm import Session
from sqlalchemy import text, select, update, delete
from models.aa_rc import AaRc

class AaRcRepository:
    def __init__(self, db: Session):
        self.db = db

    async def listar(self, esquema: str | None = None, limite: int | None = None):
        if esquema:
            self.db.execute(text(f"SET search_path TO {esquema}"))
        
        # Usando la sintaxis moderna de SQLAlchemy 2.0 (select)
        stmt = select(AaRc)
        if limite:
            stmt = stmt.limit(limite)
        
        result = self.db.execute(stmt)
        return result.scalars().all()

    async def crear(self, datos: dict, esquema: str | None = None):
        if esquema:
            self.db.execute(text(f"SET search_path TO {esquema}"))
        
        nuevo_registro = AaRc(**datos)
        self.db.add(nuevo_registro)
        self.db.commit()
        self.db.refresh(nuevo_registro)
        return True

    # IMPORTANTE: Aquí cambiamos 'id' por los dos campos de la llave compuesta
    async def eliminar(self, id_curso: int, codigo_registro: int, esquema: str | None = None):
        if esquema:
            self.db.execute(text(f"SET search_path TO {esquema}"))
        
        # Buscamos por ambos campos de la PK compuesta
        stmt = delete(AaRc).where(
            AaRc.activ_academicas_idcurso == id_curso,
            AaRc.registro_calificado_codigo == codigo_registro
        )
        
        result = self.db.execute(stmt)
        self.db.commit()
        return result.rowcount # Retorna cuántas filas se borraron (0 o 1)