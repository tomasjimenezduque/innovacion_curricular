from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .asociaciones import t_programa_ac

class AreaConocimiento(Base):
    __tablename__ = 'area_conocimiento'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gran_area: Mapped[str] = mapped_column(String(60), nullable=False)
    area: Mapped[str] = mapped_column(String(60), nullable=False)
    disciplina: Mapped[str] = mapped_column(String(60), nullable=False)

    programa: Mapped[List['Programa']] = relationship('Programa', secondary=t_programa_ac, back_populates='area_conocimiento')