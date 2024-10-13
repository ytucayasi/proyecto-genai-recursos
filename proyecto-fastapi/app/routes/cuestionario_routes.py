from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
import io
from app.services.cuestionario_service import generate_evaluation
from app.utils.pdf_utils import extract_text_from_pdf, split_text
from app.schemas.cuestionario_schema import EvaluationResponse

router = APIRouter()

@router.post("/generate_evaluation", response_model=EvaluationResponse)
async def generate_evaluation_route(
    files: List[UploadFile] = File(...),
    numero_preguntas: int = Form(...),
    numero_opciones: int = Form(...),
    dificultad: int = Form(...),
    tipo: int = Form(...)
):
    try:
        textos = []
        for file in files:
            content = await file.read()
            pdf_file = io.BytesIO(content)
            texto_completo = extract_text_from_pdf(pdf_file)
            textos.extend(split_text(texto_completo, 2048))  # Dividimos el texto en chunks

        evaluation = generate_evaluation(textos, numero_preguntas, numero_opciones, dificultad, tipo)
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))