from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .asociaciones import t_enfoque_rc

class Enfoque(Base):
    __tablename__ = 'enfoque'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(45), nullable=False)

    registro_calificado: Mapped[List['RegistroCalificado']] = relationship('RegistroCalificado', secondary=t_enfoque_rc, back_populates='enfoque')