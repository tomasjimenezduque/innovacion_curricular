import datetime
from sqlalchemy import String, Integer, Date, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Premio(Base):
    __tablename__ = 'premio'
    __table_args__ = (
        ForeignKeyConstraint(['programa'], ['programa.id'], name='premio_programa_fkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(45), nullable=False)
    fecha: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    entidad_otorgante: Mapped[str] = mapped_column(String(45), nullable=False)
    pais: Mapped[str] = mapped_column(String(45), nullable=False)
    programa: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relación inversa con Programa
    programa_: Mapped['Programa'] = relationship('Programa', back_populates='premio')