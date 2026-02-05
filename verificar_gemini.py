import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import PermissionDenied, InvalidArgument

load_dotenv()

API_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
    os.getenv("GEMINI_API_KEY_4"),
    os.getenv("GEMINI_API_KEY_5"),
]

def validar_api_key(api_key, index):
    if not api_key:
        return f"❌ Token {index}: NO DEFINIDO"

    try:
        genai.configure(api_key=api_key)

        modelos = list(genai.list_models())

        if modelos:
            return f"✅ Token {index}: VÁLIDO y ACTIVO ({len(modelos)} modelos accesibles)"
        else:
            return f"⚠️ Token {index}: VÁLIDO pero sin modelos disponibles"

    except PermissionDenied:
        return f"❌ Token {index}: REVOCADO / SIN PERMISOS"

    except InvalidArgument:
        return f"❌ Token {index}: FORMATO INVÁLIDO"

    except Exception as e:
        return f"⚠️ Token {index}: ERROR → {str(e)}"

print("\n🔍 VALIDACIÓN DE TOKENS GEMINI\n")

for i, key in enumerate(API_KEYS, start=1):
    print(validar_api_key(key, i))
