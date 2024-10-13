from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

# import openai
# from app.config import settings

# # Configura la clave de API
# openai.api_key = settings.OPENAI_API_KEY

# # Si necesitas crear un cliente específico (no necesario en este caso)
# client = openai