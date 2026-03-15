from typing import List
import datetime
from sqlalchemy import String, Integer, Date, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Facultad(Base):
    __tablename__ = 'facultad'
    __table_args__ = (
        ForeignKeyConstraint(['universidad'], ['universidad.id'], name='facultad_universidad_fkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)
    tipo: Mapped[str] = mapped_column(String(45), nullable=False)
    fecha_fun: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    universidad: Mapped[int] = mapped_column(Integer, nullable=False)

    universidad_: Mapped['Universidad'] = relationship('Universidad', back_populates='facultad')
    programa: Mapped[List['Programa']] = relationship('Programa', back_populates='facultad_')