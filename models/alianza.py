import datetime
from typing import Optional
from sqlalchemy import Integer, Date, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Alianza(Base):
    __tablename__ = 'alianza'
    __table_args__ = (
        ForeignKeyConstraint(['aliado'], ['aliado.nit'], name='alianza_aliado_fkey'),
        ForeignKeyConstraint(['departamento'], ['programa.id'], name='alianza_departamento_fkey'),
    )

    aliado: Mapped[int] = mapped_column(Integer, primary_key=True)
    departamento: Mapped[int] = mapped_column(Integer, primary_key=True) # ID del Programa
    fecha_inicio: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[Optional[datetime.date]] = mapped_column(Date)
    docente: Mapped[Optional[int]] = mapped_column(Integer)

    aliado_: Mapped['Aliado'] = relationship('Aliado', back_populates='alianza')
    programa: Mapped['Programa'] = relationship('Programa', back_populates='alianza')