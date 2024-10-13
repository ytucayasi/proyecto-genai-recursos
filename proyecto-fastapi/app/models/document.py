from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    tema = Column(String, index=True)
    malla_curricular = Column(Text)
    silabo = Column(Text)
    rubricas = Column(Text)
    content = Column(Text)
    ruta = Column(String)