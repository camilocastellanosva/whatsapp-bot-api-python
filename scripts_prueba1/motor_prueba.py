import requests
import json

# ==========================================
# 1. CREDENCIALES (¡Recuerda actualizar el Token de hoy!)
# ==========================================
TOKEN = "EAAYwRcF4k60BSdr2ZCOA5bBTZCiMjcb1dTLfYEVvERtVYikPzI5z61t6aYUbhhYGG2x4mCYHixixQb3FuRAVK75MTqhTEbSGAmqNxORsBca66HfdEUSHRZA8Xf4iOlfDtFVXZC55hG1ZBoAuVt8ZBREoNraq5nwmt1Ek6JQJZBpAfTUWURZAEZAijBB8fZBLoZBT8idj4wTvDmoRpwaRRJuW94kH81bxYonUnz7b1qLxoZCKV0fzq6XTGAQXvg72HufpMwAoFguZAb5qTOv9FdNEdoZA8IUwIl"
PHONE_NUMBER_ID = "1303528422837098"

# ==========================================
# 2. FUNCIÓN PARA ENVIAR LA PLANTILLA
# ==========================================
def enviar_plantilla(numero_destino, nombre_cliente, rubro_empresa):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": numero_destino,
        "type": "template",
        "template": {
            "name": "template_contacto1", # <-- ¡Cámbialo! Ej: invitacion_cumbre
            "language": {
                "code": "es_CO" # <-- ¡Cámbialo si Meta te puso es_CO o es_LA!
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": nombre_cliente}, # Reemplaza el {{1}}
                        {"type": "text", "text": rubro_empresa}   # Reemplaza el {{2}}
                    ]
                }
            ]
        }
    }

    respuesta = requests.post(url, headers=headers, json=data)
    print(f"🚀 Respuesta de Meta al enviar plantilla: {respuesta.json()}")

# ==========================================
# 3. EJECUCIÓN DE PRUEBA
# ==========================================
# Pon aquí tu número de celular (el mismo con el que probamos ayer)
numero_prueba = "573025489729" 

# Aquí simulamos los datos que luego sacaremos del Excel
enviar_plantilla(numero_prueba, "Camilo", "tecnología y software")