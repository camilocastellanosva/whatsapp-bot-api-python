import requests
import json

TOKEN = "EABCrw4riEjoBSMKoPpvZAtMUJ7l5BZAUZCdbKMcAkNctWUhqY1N9PjPkIV4qkoLcbAvEMAKysDouKbZArJKM3mJ9kHN0QF7sNjaEgIdidBrbbQQrnVyxfWx4PeV3PcZC3PUaYKZCjgGIwaEAO5sgqCNInHZBUM922vj2voAZBPfejj67tgBovKzAUnkHUZCaUDGZCWFOLCOGPWGykqyPKnjlUgpZAkSK27JohQ4k4ZAyCIIvkcEtjXscY2R7AVRRz605NRZBZBXO2RmpzZBo15c6PGkGyTseDwp"
PHONE_NUMBER_ID = 1244993902032511
NUMERO_DESTINO = 573025489729


url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "messaging_product": "whatsapp",
    "to": NUMERO_DESTINO,
    "type": "template",
    "template": {
        "name": "hello_world",
        "language": {
            "code": "en_US"
        }
    }
}

print("Enviando mensaje...")
respuesta = requests.post(url, headers=headers, json=data)

if respuesta.status_code == 200:
    print("✅ ¡Mensaje enviado con éxito desde Python!")
else:
    print("❌ Hubo un error al enviar el mensaje:")
    print(respuesta.json())