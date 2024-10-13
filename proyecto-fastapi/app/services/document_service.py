from app.core.openai_client import client
import re
from docx import Document
from datetime import datetime
import os
import openai

OUTPUT_DIR = "genai"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_content(text):
    text = re.sub(r'#+\s', '', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'^\d+\.\s', '', text, flags=re.MULTILINE)
    return text.strip()

def generate_content(data):
    prompt = f"""
    Genera un informe académico estructurado utilizando la siguiente información:

    1. Título: {data.tema}

    2. Introducción:
    Redacta una introducción sobre el tema {data.tema}, relacionándolo con la malla curricular {data.malla_curricular}, el sílabo {data.silabo} y las rúbricas {data.rubricas}. Si es relevante, incluye una perspectiva desde un punto de vista adventista.

    3. Contenido principal:
    Desarrolla el contenido en detalle utilizando el tema {data.tema}, la malla curricular {data.malla_curricular}, el sílabo {data.silabo} y las rúbricas {data.rubricas}. Proporciona un análisis profundo y ejemplos donde sea apropiado.

    4. Conclusión:
    Escribe una conclusión que integre los aspectos principales del tema {data.tema}, la malla curricular {data.malla_curricular}, el sílabo {data.silabo} y las rúbricas {data.rubricas}. Finaliza con una reflexión, y si es aplicable, incluye una perspectiva desde un punto de vista adventista.

    Separa cada sección (Título, Introducción, Contenido principal, Conclusión) con '==='.
    No uses formato Markdown ni caracteres especiales para dar formato al texto.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente académico experto en generar informes estructurados sin formato especial."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500,
    )
    content = response.choices[0].message.content.strip()
    return '\n===\n'.join(clean_content(part) for part in content.split('==='))

def create_document_from_template(content, template_path, output_file):
    doc = Document(template_path)

    parts = content.split('===')
    titulo = parts[0].strip() if len(parts) > 0 else ""
    introduccion = parts[1].strip() if len(parts) > 1 else ""
    contenido_principal = parts[2].strip() if len(parts) > 2 else ""
    conclusion = parts[3].strip() if len(parts) > 3 else ""

    for paragraph in doc.paragraphs:
        if '[titulo]' in paragraph.text:
            paragraph.text = paragraph.text.replace('[titulo]', titulo)
        if '[fechaActual]' in paragraph.text:
            paragraph.text = paragraph.text.replace('[fechaActual]', datetime.now().strftime("%d/%m/%Y"))
        if '[textoIntroduccion]' in paragraph.text:
            paragraph.text = paragraph.text.replace('[textoIntroduccion]', introduccion)
        if '[contenido]' in paragraph.text:
            paragraph.text = paragraph.text.replace('[contenido]', contenido_principal)
        if '[contenidoConclusion]' in paragraph.text:
            paragraph.text = paragraph.text.replace('[contenidoConclusion]', conclusion)

    doc.save(output_file)
    return output_file