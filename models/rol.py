import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Text, Boolean, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .asociaciones import t_rol_usuario

class Rol(Base):
    __tablename__ = 'rol'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    fecha_creacion: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    usuario: Mapped[List['Usuario']] = relationship('Usuario', secondary=t_rol_usuario, back_populates='rol')