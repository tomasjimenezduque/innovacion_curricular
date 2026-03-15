from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Aliado(Base):
    __tablename__ = 'aliado'

    nit: Mapped[int] = mapped_column(Integer, primary_key=True)
    razon_social: Mapped[str] = mapped_column(String(60), nullable=False)
    nombre_contacto: Mapped[str] = mapped_column(String(60), nullable=False)
    correo: Mapped[str] = mapped_column(String(70), nullable=False)
    telefono: Mapped[str] = mapped_column(String(45), nullable=False)
    ciudad: Mapped[str] = mapped_column(String(45), nullable=False)

    # Relación con la tabla intermedia Alianza
    alianza: Mapped[List['Alianza']] = relationship('Alianza', back_populates='aliado_')