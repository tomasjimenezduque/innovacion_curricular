from typing import List
from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .asociaciones import t_programa_ci

class CarInnovacion(Base):
    __tablename__ = 'car_innovacion'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    tipo: Mapped[str] = mapped_column(String(45), nullable=False)

    programa: Mapped[List['Programa']] = relationship('Programa', secondary=t_programa_ci, back_populates='car_innovacion')