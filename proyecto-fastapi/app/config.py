from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # FastAPI
    SECRET_KEY: str

    # OpenAI
    OPENAI_API_KEY: str

    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:4200"]  # Puedes ajustar esto según tus necesidades

    class Config:
        env_file = ".env"

settings = Settings()