from fastapi import APIRouter, HTTPException
from app.schemas.presentation import PresentationRequest
from app.services.presentation_service import create_ppt_text, create_ppt
import os

router = APIRouter()

@router.post("/generate")
async def generate_presentation(request: PresentationRequest):
    user_text = request.msg
    selected_design = request.design
    slide_count = request.slides or 8

    if not user_text:
        raise HTTPException(status_code=400, detail="No message provided")
    
    design_number = int(selected_design) if selected_design else 1
    if design_number > 10 or design_number == 0:
        design_number = 1

    try:
        ppt_text = create_ppt_text(user_text)
        filename = f"presentation_{os.urandom(8).hex()}"            
        with open(f'Cache/{filename}', 'w', encoding='utf-8') as f:
            f.write(ppt_text)
        paths = create_ppt(f'Cache/{filename}', design_number, filename, slide_count)
        return paths
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{file_type}/{path:path}")
async def download_file(file_type: str, path: str):
    if file_type not in ["pptx", "pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    directory = "GeneratedPresentations" if file_type == "pptx" else "GeneratedPdf"
    file_path = f'{directory}/{path}'
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, filename=path)