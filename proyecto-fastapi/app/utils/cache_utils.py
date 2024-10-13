import os
import json
import hashlib

def get_cache_key(textos, numero_preguntas, numero_opciones, dificultad, tipo):
    input_string = f"{'-'.join(textos)}_{numero_preguntas}_{numero_opciones}_{dificultad}_{tipo}"
    return hashlib.sha256(input_string.encode()).hexdigest()

def get_cached_response(key):
    if not os.path.exists("cache"):
        return None
    cache_file = f"cache/{key}.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    return None

def save_to_cache(key, response):
    if not os.path.exists("cache"):
        os.makedirs("cache")
    cache_file = f"cache/{key}.json"
    with open(cache_file, "w") as f:
        json.dump(response, f)