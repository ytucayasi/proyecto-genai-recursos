from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routes import cuestionario_routes, document, presentation_routes
from app.config import settings
from fastapi.responses import JSONResponse
import time
from collections import defaultdict
import os

# Crea las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GenAIRec API",
    description="API para generación de evaluaciones y presentaciones usando IA",
    version="1.0.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Implementación simple de limitación de tasa
class RateLimiter:
    def __init__(self, calls, period):
        self.calls = calls
        self.period = period
        self.clock = time.monotonic
        self.last_reset = self.clock()
        self.num_calls = defaultdict(int)

    async def is_rate_limited(self, key):
        now = self.clock()
        if now - self.last_reset > self.period:
            self.num_calls.clear()
            self.last_reset = now

        self.num_calls[key] += 1
        return self.num_calls[key] > self.calls

rate_limiter = RateLimiter(calls=50, period=86400)  # 10 calls per day

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    if await rate_limiter.is_rate_limited(client_ip):
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
    response = await call_next(request)
    return response

# Montar directorios para archivos estáticos
app.mount("/GeneratedPresentations", StaticFiles(directory="GeneratedPresentations"), name="generated_presentations")
app.mount("/GeneratedPdf", StaticFiles(directory="GeneratedPdf"), name="generated_pdf")

# Asegúrate de que los directorios existan
os.makedirs("GeneratedPresentations", exist_ok=True)
os.makedirs("GeneratedPdf", exist_ok=True)

app.include_router(cuestionario_routes.router, prefix="/cuestionario", tags=["cuestionario"])
app.include_router(document.router, prefix="/documents", tags=["documents"])
app.include_router(presentation_routes.router, prefix="/presentation", tags=["presentation"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a GenAIRec API"}