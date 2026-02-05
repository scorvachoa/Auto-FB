import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# -----------------------------
# Carga de entorno
# -----------------------------
load_dotenv()

MODEL_NAME = "gemini-2.5-flash"
INDEX_FILE = "gemini_index.json"

# -----------------------------
# Cargar API Keys (pool)
# -----------------------------
API_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
    os.getenv("GEMINI_API_KEY_4"),
    os.getenv("GEMINI_API_KEY_5"),
]

API_KEYS = [k for k in API_KEYS if k]

if not API_KEYS:
    raise RuntimeError("❌ No hay GEMINI_API_KEY_x definidas en el .env")

# -----------------------------
# Rotación secuencial de keys
# -----------------------------
def obtener_siguiente_key():
    index = 0

    if os.path.exists(INDEX_FILE):
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                index = json.load(f).get("index", 0)
        except Exception:
            index = 0

    key = API_KEYS[index % len(API_KEYS)]

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump({"index": index + 1}, f)

    return key

# -----------------------------
# Limpieza y normalización del copy
# -----------------------------
def limpiar_copy(texto: str) -> str:
    lineas = texto.splitlines()

    filtradas = []
    for linea in lineas:
        l = linea.lower()
        if any(x in l for x in [
            "aquí tienes",
            "claro",
            "texto publicitario",
            "publicación para facebook",
            "---"
        ]):
            continue
        filtradas.append(linea)

    texto_limpio = "\n".join(filtradas).strip()

    # Extraer hashtags
    hashtags = re.findall(r"#\w+", texto_limpio)

    # Forzar EXACTAMENTE 5 hashtags
    if len(hashtags) > 5:
        for h in hashtags[5:]:
            texto_limpio = texto_limpio.replace(h, "")
    elif len(hashtags) < 5:
        faltantes = 5 - len(hashtags)
        extras = ["#Turismo", "#Viajes", "#Aventura", "#Descubre", "#Naturaleza"]
        for h in extras[:faltantes]:
            texto_limpio += f" {h}"

    return texto_limpio.strip()

# -----------------------------
# Generación principal del copy
# -----------------------------
def generar_copy(ruta_foto: str) -> str:
    prompt = """
Genera ÚNICAMENTE el texto final de una publicación turística para Facebook en español,
basado en la imagen proporcionada.

REGLAS ESTRICTAS:
- NO incluyas introducciones ni explicaciones
- NO uses títulos, listas ni separadores
- Devuelve SOLO el texto listo para publicar
- Tono turístico, inspirador y emocional
- Usa emojis relevantes y naturales según la imagen (viajes, paisajes, cultura, aventura)
- Longitud: 3 a 5 líneas
- Incluye EXACTAMENTE 5 hashtags turísticos relevantes al final
"""

    for _ in range(len(API_KEYS)):
        try:
            api_key = obtener_siguiente_key()
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(MODEL_NAME)

            imagen = Image.open(ruta_foto)
            respuesta = model.generate_content([prompt, imagen])

            texto = respuesta.text.strip()
            if texto:
                return limpiar_copy(texto)

        except Exception as e:
            print(f"⚠️ Gemini falló con una API key, rotando… ({e})")

    # Fallback final (nunca deja vacío)
    return (
        "🌄 Viajar es descubrir paisajes que te dejan sin palabras y momentos que se quedan "
        "para siempre en la memoria. Cada rincón invita a detenerse, respirar y conectar "
        "con la esencia del lugar. ✨\n\n"
        "#Turismo #Viajes #Aventura #Descubre #Naturaleza"
    )
