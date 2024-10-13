import json
from typing import List
from openai import OpenAI
from app.utils.pdf_utils import num_tokens_from_string
from app.utils.cache_utils import get_cache_key, get_cached_response, save_to_cache
from fastapi import HTTPException
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 4096

def generate_prompt(textos: List[str], numero_preguntas: int, numero_opciones: int, dificultad: int, tipo: int) -> str:
    dificultades = ["fácil", "medio", "difícil"]
    tipos = ["mixto", "solo opciones", "solo preguntas libres", "verdadero y falso"]
    
    prompt = f"""Crea una evaluación basada en los siguientes textos:

"""

    for i, texto in enumerate(textos):
        prompt += f"Texto {i+1}:\n{texto}\n\n"

    prompt += f"""Características de la evaluación:
- Número total de preguntas: {numero_preguntas}
- Nivel de dificultad: {dificultades[dificultad]}
- Tipo de preguntas: {tipos[tipo]}
"""

    if tipo == 0:  # mixto
        prompt += f"""
- Para preguntas de opción múltiple, usa {numero_opciones} opciones.
- Mezcla preguntas de opción múltiple, preguntas abiertas y verdadero/falso.
"""
    elif tipo == 1:  # solo opciones
        prompt += f"""
- Todas las preguntas deben ser de opción múltiple con {numero_opciones} opciones.
"""
    elif tipo == 2:  # solo preguntas libres
        prompt += """
- Todas las preguntas deben ser abiertas, para responder textualmente.
"""
    elif tipo == 3:  # verdadero y falso
        prompt += """
- Todas las preguntas deben ser de tipo verdadero o falso.
"""

    prompt += f"""
Distribuye las preguntas equitativamente entre los {len(textos)} textos proporcionados.
Asegúrate de que cada texto tenga al menos una pregunta si es posible.

Formato de respuesta:
{{
    "preguntas": [
        {{
            "tipo": "opcion_multiple",
            "pregunta": "Texto de la pregunta",
            "opciones": ["Opción A", "Opción B", "Opción C"],
            "respuesta_correcta": 0,
            "texto_fuente": 1
        }},
        {{
            "tipo": "abierta",
            "pregunta": "Texto de la pregunta",
            "respuesta_sugerida": "Una posible respuesta correcta",
            "texto_fuente": 2
        }},
        {{
            "tipo": "verdadero_falso",
            "pregunta": "Texto de la pregunta",
            "respuesta_correcta": true,
            "texto_fuente": 1
        }}
    ]
}}
"""
    return prompt

def generate_evaluation(textos: List[str], numero_preguntas: int, numero_opciones: int, dificultad: int, tipo: int):
    try:
        cache_key = get_cache_key(textos, numero_preguntas, numero_opciones, dificultad, tipo)
        cached_response = get_cached_response(cache_key)
        if cached_response:
            return {"evaluation": cached_response, "source": "cache"}

        prompt = generate_prompt(textos, numero_preguntas, numero_opciones, dificultad, tipo)
        prompt_tokens = num_tokens_from_string(prompt, "cl100k_base")

        if prompt_tokens > MAX_TOKENS:
            raise HTTPException(status_code=400, detail="El texto es demasiado largo para procesar en una sola solicitud")

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Eres un asistente especializado en crear evaluaciones educativas."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=MAX_TOKENS - prompt_tokens
        )
        generated_evaluation = json.loads(response.choices[0].message.content)

        save_to_cache(cache_key, generated_evaluation)

        return {"evaluation": generated_evaluation, "source": "openai"}
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="Error al procesar la respuesta de OpenAI")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))