from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .asociaciones import t_an_programa

class AspectoNormativo(Base):
    __tablename__ = 'aspecto_normativo'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo: Mapped[str] = mapped_column(String(45), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(45), nullable=False)
    fuente: Mapped[str] = mapped_column(String(45), nullable=False)

    programa: Mapped[List['Programa']] = relationship('Programa', secondary=t_an_programa, back_populates='aspecto_normativo')