from pydantic import BaseModel
from typing import List, Optional

class Question(BaseModel):
    tipo: str
    pregunta: str
    opciones: Optional[List[str]] = None
    respuesta_correcta: Optional[int] = None
    respuesta_sugerida: Optional[str] = None
    texto_fuente: int

class Evaluation(BaseModel):
    preguntas: List[Question]

class EvaluationResponse(BaseModel):
    evaluation: Evaluation
    source: str