import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def generar_copy(ruta_foto: str):
    prompt = """
    Crea un texto publicitario breve y atractivo en español para una publicación en Facebook
    basado en la imagen proporcionada.
    El texto debe sonar humano, emocional y tener 3 hashtags relevantes al final.
    """
    try:
        imagen = Image.open(ruta_foto)
        respuesta = model.generate_content([prompt, imagen])
        return respuesta.text.strip()
    except Exception as e:
        print(f"⚠️ Error generando copy con Gemini: {e}")
        return "Vive cada momento con pasión. #Inspírate #Vida #Belleza"
