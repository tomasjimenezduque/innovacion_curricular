import datetime
from typing import Optional
from sqlalchemy import String, Integer, Date, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class DocenteDepartamento(Base):
    __tablename__ = 'docente_departamento'
    __table_args__ = (
        ForeignKeyConstraint(['departamento'], ['programa.id'], name='docente_departamento_departamento_fkey'),
    )

    docente: Mapped[int] = mapped_column(Integer, primary_key=True)
    departamento: Mapped[int] = mapped_column(Integer, primary_key=True) # ID del Programa
    dedicacion: Mapped[str] = mapped_column(String(15), nullable=False)
    modalidad: Mapped[str] = mapped_column(String(45), nullable=False)
    fecha_ingreso: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    fecha_salida: Mapped[Optional[datetime.date]] = mapped_column(Date)

    programa: Mapped['Programa'] = relationship('Programa', back_populates='docente_departamento')