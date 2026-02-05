import os
import json
import random
import requests
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from generar_copy import generar_copy

load_dotenv()

CARPETA_FOTOS = "fotos"
ARCHIVO_REGISTRO = "publicadas.json"

PAGE_ID = os.getenv("FB_PAGE_ID")
ACCESS_TOKEN = os.getenv("FB_SYSTEM_USER_TOKEN")

# -----------------------------------
# Validación inicial
# -----------------------------------

if not PAGE_ID or not ACCESS_TOKEN:
    raise RuntimeError("❌ Falta FB_PAGE_ID o FB_SYSTEM_USER_TOKEN en el .env")

# -----------------------------------
# Utilidades
# -----------------------------------

def obtener_page_access_token():
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}"
    params = {
        "fields": "access_token",
        "access_token": ACCESS_TOKEN
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "error" in data:
        raise Exception(data["error"]["message"])

    return data["access_token"]

def generar_fecha_programada(dias_desde_hoy: int):
    base = datetime.now() + timedelta(days=dias_desde_hoy)

    hora = random.randint(10, 16)
    minuto = random.randint(0, 59)

    fecha = base.replace(
        hour=hora,
        minute=minuto,
        second=0,
        microsecond=0
    )

    return int(fecha.timestamp())

def cargar_publicadas():
    if not os.path.exists(ARCHIVO_REGISTRO):
        return []

    with open(ARCHIVO_REGISTRO, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def guardar_publicacion(nombre, fecha_creacion_programacion, fecha_publicacion_programada):
    publicadas = cargar_publicadas()

    publicadas.append({
        "foto": nombre,
        "fecha_creacion_programacion": fecha_creacion_programacion,
        "fecha_publicacion_programada": fecha_publicacion_programada
    })

    with open(ARCHIVO_REGISTRO, "w", encoding="utf-8") as f:
        json.dump(publicadas, f, indent=2, ensure_ascii=False)

def elegir_foto():
    usadas = [x["foto"] for x in cargar_publicadas()]

    if not os.path.exists(CARPETA_FOTOS):
        raise RuntimeError(f"❌ No existe la carpeta {CARPETA_FOTOS}")

    fotos = [
        f for f in os.listdir(CARPETA_FOTOS)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    disponibles = [f for f in fotos if f not in usadas]
    return random.choice(disponibles) if disponibles else None

# -----------------------------------
# Publicación
# -----------------------------------

def publicar_en_facebook(foto_path, mensaje, scheduled_time=None):
    page_token = obtener_page_access_token()
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/photos"

    with open(foto_path, "rb") as img:
        files = {"source": img}
        data = {
            "caption": mensaje,
            "access_token": page_token
        }

        if scheduled_time:
            data["published"] = "false"
            data["scheduled_publish_time"] = scheduled_time

        response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        print("⏰ Publicación programada correctamente.")
        return True
    else:
        print("❌ Error al publicar")
        print(response.text)
        return False

# -----------------------------------
# Flujo principal
# -----------------------------------

def programar_publicaciones(dias=5):
    print(f"📆 Programando publicaciones para {dias} días...\n")

    fecha_ejecucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for i in range(1, dias + 1):
        foto = elegir_foto()
        if not foto:
            print("🎉 No hay más fotos disponibles.")
            break

        ruta_foto = os.path.join(CARPETA_FOTOS, foto)
        copy = generar_copy(ruta_foto)

        scheduled_time = generar_fecha_programada(i)
        fecha_legible = datetime.fromtimestamp(scheduled_time)
        fecha_programada_str = fecha_legible.strftime("%Y-%m-%d %H:%M:%S")

        print(f"🗓 {foto} → {fecha_programada_str}")

        ok = publicar_en_facebook(
            ruta_foto,
            copy,
            scheduled_time=scheduled_time
        )

        if ok:
            guardar_publicacion(
                nombre=foto,
                fecha_creacion_programacion=fecha_ejecucion,
                fecha_publicacion_programada=fecha_programada_str
            )

        time.sleep(2)  # evita rate-limit

# -----------------------------------
# Entry point
# -----------------------------------

if __name__ == "__main__":
    programar_publicaciones(dias=5)
