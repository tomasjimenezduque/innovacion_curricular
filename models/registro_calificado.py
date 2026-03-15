import datetime
from typing import List
from sqlalchemy import String, Integer, Date, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .asociaciones import t_enfoque_rc

class RegistroCalificado(Base):
    __tablename__ = 'registro_calificado'
    __table_args__ = (
        ForeignKeyConstraint(['programa'], ['programa.id'], name='registro_calificado_programa_fkey'),
    )

    codigo: Mapped[int] = mapped_column(Integer, primary_key=True)
    cant_creditos: Mapped[str] = mapped_column(String(45), nullable=False)
    hora_acom: Mapped[str] = mapped_column(String(45), nullable=False)
    hora_ind: Mapped[str] = mapped_column(String(45), nullable=False)
    metodologia: Mapped[str] = mapped_column(String(45), nullable=False)
    fecha_inicio: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    duracion_anios: Mapped[str] = mapped_column(String(45), nullable=False)
    duracion_semestres: Mapped[str] = mapped_column(String(45), nullable=False)
    tipo_titulacion: Mapped[str] = mapped_column(String(45), nullable=False)
    programa: Mapped[int] = mapped_column(Integer, nullable=False)

    programa_: Mapped['Programa'] = relationship('Programa', back_populates='registro_calificado')
    enfoque: Mapped[List['Enfoque']] = relationship('Enfoque', secondary=t_enfoque_rc, back_populates='registro_calificado')
    aa_rc: Mapped[List['AaRc']] = relationship('AaRc', back_populates='registro_calificado')