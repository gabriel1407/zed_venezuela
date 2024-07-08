from sqlalchemy import Column, Integer, String
from db.db import Base

class Saludo(Base):
    __tablename__ = 'saludos'
    id = Column(Integer, primary_key=True, index=True)
    mensaje = Column(String(255), index=True)
