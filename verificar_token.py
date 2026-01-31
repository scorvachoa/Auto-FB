import os
import requests
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

ACCESS_TOKEN = os.getenv("FB_SYSTEM_USER_TOKEN")
PAGE_ID = os.getenv("FB_PAGE_ID")

def verificar_token_y_pagina():
    print("🔍 Verificando token de Facebook...\n")

    if not ACCESS_TOKEN or not PAGE_ID:
        print("❌ Falta el token o el PAGE_ID en el archivo .env")
        return

    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}"
    params = {
        "fields": "name,id",
        "access_token": ACCESS_TOKEN
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "error" in data:
            print("❌ Token inválido o sin permisos")
            print(f"Detalle: {data['error']['message']}")
            return

        print("✅ TOKEN VÁLIDO Y FUNCIONANDO\n")
        print("📄 Página accesible:")
        print(f"🆔 ID: {data.get('id')}")
        print(f"📛 Nombre: {data.get('name')}")

    except Exception as e:
        print("⚠️ Error inesperado:", e)

if __name__ == "__main__":
    verificar_token_y_pagina()
