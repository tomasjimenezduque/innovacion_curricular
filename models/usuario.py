from typing import Optional, List
import datetime
from sqlalchemy import String, Boolean, DateTime, text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .asociaciones import t_rol_usuario

class Usuario(Base):
    __tablename__ = 'usuario'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    nombre_completo: Mapped[Optional[str]] = mapped_column(String(200))
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    fecha_creacion: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    # Relación Many-to-Many con Rol usando la tabla intermedia
    rol: Mapped[List['Rol']] = relationship('Rol', secondary=t_rol_usuario, back_populates='usuario')