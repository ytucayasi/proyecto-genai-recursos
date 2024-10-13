from fastapi import FastAPI
from app.database import engine, Base

# Crea las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

""" app.include_router(users.router, prefix="/users", tags=["users"]) """

@app.get("/")
def read_root():
    return {"Hello": "World"}