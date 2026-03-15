from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .asociaciones import t_programa_pe

class PracticaEstrategia(Base):
    __tablename__ = 'practica_estrategia'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo: Mapped[str] = mapped_column(String(45), nullable=False)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(45), nullable=False)

    programa: Mapped[List['Programa']] = relationship('Programa', secondary=t_programa_pe, back_populates='practica_estrategia')