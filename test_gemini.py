import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

PROMPT = (
    "Crea un texto publicitario breve y atractivo en español para una "
    "publicación en Facebook. El texto debe sonar humano, emocional y "
    "tener 3 hashtags relevantes al final."
)

API_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
    os.getenv("GEMINI_API_KEY_4"),
    os.getenv("GEMINI_API_KEY_5"),
]

def obtener_modelo_texto():
    """
    Devuelve el primer modelo que soporte generateContent
    """
    for model in genai.list_models():
        if "generateContent" in model.supported_generation_methods:
            return model.name
    return None

def generar_con_token(api_key, index):
    if not api_key:
        return f"❌ Token {index}: NO DEFINIDO\n"

    try:
        genai.configure(api_key=api_key)

        modelo_nombre = obtener_modelo_texto()

        if not modelo_nombre:
            return f"❌ Token {index}: NO HAY MODELOS COMPATIBLES\n"

        model = genai.GenerativeModel(modelo_nombre)
        response = model.generate_content(PROMPT)

        return (
            f"\n🟢 TOKEN {index} — MODELO: {modelo_nombre}\n"
            f"{response.text.strip()}\n"
            f"{'-'*60}"
        )

    except Exception as e:
        return f"⚠️ Token {index}: ERROR → {str(e)}\n"

print("\n📣 GENERACIÓN DE TEXTOS PUBLICITARIOS (FACEBOOK)\n")

for i, key in enumerate(API_KEYS, start=1):
    print(generar_con_token(key, i))
