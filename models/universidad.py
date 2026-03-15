from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Universidad(Base):
    __tablename__ = 'universidad'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)
    tipo: Mapped[str] = mapped_column(String(45), nullable=False)
    ciudad: Mapped[str] = mapped_column(String(45), nullable=False)

    facultad: Mapped[List['Facultad']] = relationship('Facultad', back_populates='universidad_')