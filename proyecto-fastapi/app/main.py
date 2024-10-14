from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import cuestionario_routes
from app.config import settings
from app.routes import document

# Crea las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GenAIRec API",
    description="API para generación de evaluaciones usando IA",
    version="1.0.0",
)

# Configurar CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cuestionario_routes.router, prefix="/cuestionario", tags=["cuestionario"])
app.include_router(document.router, prefix="/documents", tags=["documents"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a GenAIRec API"}