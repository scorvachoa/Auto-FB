import requests
from config import FB_PAGE_ID, FB_ACCESS_TOKEN, FOLDER_FOTOS
import os

def publicar_en_facebook(nombre_foto, copy):
    ruta = os.path.join(FOLDER_FOTOS, nombre_foto)
    if not os.path.exists(ruta):
        print(f"❌ No se encontró la imagen: {ruta}")
        return

    url = f"https://graph.facebook.com/{FB_PAGE_ID}/photos"
    payload = {
        "message": copy,
        "access_token": FB_ACCESS_TOKEN
    }

    with open(ruta, "rb") as img:
        files = {"source": img}
        r = requests.post(url, data=payload, files=files)

    if r.status_code == 200:
        print(f"✅ Publicación exitosa: {nombre_foto}")
    else:
        print(f"⚠️ Error al publicar: {r.text}")
