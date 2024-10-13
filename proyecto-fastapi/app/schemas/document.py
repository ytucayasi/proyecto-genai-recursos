from pydantic import BaseModel, ConfigDict

class DocumentBase(BaseModel):
    tema: str
    malla_curricular: str
    silabo: str
    rubricas: str

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    content: str
    ruta: str

    # class Config:
    #     orm_mode = True

    model_config = ConfigDict(from_attributes=True)