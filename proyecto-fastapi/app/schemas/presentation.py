from pydantic import BaseModel
from typing import Optional

class PresentationRequest(BaseModel):
    msg: str
    design: Optional[str] = None
    slides: Optional[int] = None