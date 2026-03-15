from sqlalchemy import String, Integer, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Pasantia(Base):
    __tablename__ = 'pasantia'
    __table_args__ = (
        ForeignKeyConstraint(['programa'], ['programa.id'], name='pasantia_programa_fkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    pais: Mapped[str] = mapped_column(String(45), nullable=False)
    empresa: Mapped[str] = mapped_column(String(45), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(45), nullable=False)
    programa: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relación inversa con Programa
    programa_: Mapped['Programa'] = relationship('Programa', back_populates='pasantia')