from typing import List, TYPE_CHECKING
from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from .base import Base


class Aliado(Base):
    __tablename__ = 'aliado'

    nit = Column(String, primary_key=True)
    razon_social: Mapped[str] = mapped_column(String(60), nullable=False)
    nombre_contacto: Mapped[str] = mapped_column(String(60), nullable=False)
    correo: Mapped[str] = mapped_column(String(70), nullable=False)
    telefono: Mapped[str] = mapped_column(String(45), nullable=False)
    ciudad: Mapped[str] = mapped_column(String(45), nullable=False)

    # Relación con la tabla intermedia Alianza
    alianzas: Mapped[List["Alianza"]] = relationship("Alianza", back_populates="aliado_")

from models.alianza import Alianza