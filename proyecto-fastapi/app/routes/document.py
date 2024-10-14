from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.schemas.document import DocumentCreate, Document
from app.models.document import Document as DocumentModel
from app.services.document_service import generate_content, create_document_from_template
import os

router = APIRouter()

@router.post("/generate_word", response_model=Document)
async def generate_word(data: DocumentCreate, db: Session = Depends(get_db)):
    try:
        # Generar el contenido
        generated_content = generate_content(data)

        # Definir el nombre y la ruta del archivo
        word_filename = f"{data.tema.replace(' ', '_')}.docx"
        word_file = os.path.join("genai", word_filename)

        # Crear el documento desde la plantilla
        create_document_from_template(generated_content, "plantilla1.docx", word_file)

        # Crear el modelo de documento
        new_document = DocumentModel(
            tema=data.tema,
            malla_curricular=data.malla_curricular,
            silabo=data.silabo,
            rubricas=data.rubricas,
            content=generated_content,
            ruta=word_file  # Aquí asignas la ruta
        )

        # Guardar en la base de datos
        db.add(new_document)
        db.commit()
        db.refresh(new_document)

        return Document.from_orm(new_document)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[Document])
async def get_documents(db: Session = Depends(get_db)):
    try:
        documents = db.query(DocumentModel).order_by(desc(DocumentModel.id)).all()
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/download/{filename}")
async def download_file(filename: str):
    # Construir la ruta para el archivo en el directorio genai
    file_path = os.path.join("genai", filename)

    # Verificar si el archivo existe
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        file_path, 
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
        filename=filename
    )