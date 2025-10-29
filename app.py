import os
import json
import random
import requests
from datetime import datetime
from dotenv import load_dotenv
from generar_copy import generar_copy

load_dotenv()

CARPETA_FOTOS = "fotos"
ARCHIVO_REGISTRO = "publicadas.json"
PAGE_ID = os.getenv("PAGE_ID")
ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")

# -----------------------------------
# Utilidades
# -----------------------------------

def cargar_publicadas():
    if not os.path.exists(ARCHIVO_REGISTRO):
        return []
    with open(ARCHIVO_REGISTRO, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def guardar_publicada(nombre):
    publicadas = cargar_publicadas()
    publicadas.append({"foto": nombre, "fecha": datetime.now().isoformat()})
    with open(ARCHIVO_REGISTRO, "w", encoding="utf-8") as f:
        json.dump(publicadas, f, indent=2, ensure_ascii=False)

def elegir_foto():
    usadas = [x["foto"] for x in cargar_publicadas()]
    fotos = [f for f in os.listdir(CARPETA_FOTOS) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    disponibles = [f for f in fotos if f not in usadas]
    return random.choice(disponibles) if disponibles else None

# -----------------------------------
# Publicación
# -----------------------------------

def publicar_en_facebook(foto_path, mensaje):
    url = f"https://graph.facebook.com/{PAGE_ID}/photos"
    with open(foto_path, "rb") as img:
        files = {"source": img}
        data = {"caption": mensaje, "access_token": ACCESS_TOKEN}
        response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        print("✅ Publicación exitosa en Facebook.")
    else:
        print(f"⚠️ Error al publicar: {response.text}")

# -----------------------------------
# Flujo principal (publicación inmediata)
# -----------------------------------

def publicar_ahora():
    print("🚀 Ejecutando publicación inmediata...\n")

    foto = elegir_foto()
    if not foto:
        print("🎉 No hay fotos nuevas para publicar.")
        return

    ruta_foto = os.path.join(CARPETA_FOTOS, foto)
    print(f"🎯 Foto seleccionada: {foto}")

    copy = generar_copy(ruta_foto)
    print(f"\n📝 Copy generado:\n{copy}\n")

    publicar_en_facebook(ruta_foto, copy)
    guardar_publicada(foto)

    print(f"📸 Publicación completada: {foto}")
    print("✅ Fin del proceso.")

if __name__ == "__main__":
    publicar_ahora()
