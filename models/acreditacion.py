from sqlalchemy import String, Integer, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Acreditacion(Base):
    __tablename__ = 'acreditacion'
    __table_args__ = (
        ForeignKeyConstraint(['programa'], ['programa.id'], name='acreditacion_programa_fkey'),
    )

    resolucion: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo: Mapped[str] = mapped_column(String(45), nullable=False)
    calificacion: Mapped[str] = mapped_column(String(45), nullable=False)
    fecha_inicio: Mapped[str] = mapped_column(String(45), nullable=False)
    fecha_fin: Mapped[str] = mapped_column(String(45), nullable=False)
    programa: Mapped[int] = mapped_column(Integer, nullable=False)

    programa_: Mapped['Programa'] = relationship('Programa', back_populates='acreditacion')