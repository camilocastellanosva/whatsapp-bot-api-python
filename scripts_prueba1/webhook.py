from flask import Flask, request
import requests

app = Flask(__name__)
VERIFY_TOKEN = "mi_token_secreto_sigamed"

# ==========================================
# 1. CREDENCIALES DE META
# ==========================================
TOKEN = "EAAYwRcF4k60BSdr2ZCOA5bBTZCiMjcb1dTLfYEVvERtVYikPzI5z61t6aYUbhhYGG2x4mCYHixixQb3FuRAVK75MTqhTEbSGAmqNxORsBca66HfdEUSHRZA8Xf4iOlfDtFVXZC55hG1ZBoAuVt8ZBREoNraq5nwmt1Ek6JQJZBpAfTUWURZAEZAijBB8fZBLoZBT8idj4wTvDmoRpwaRRJuW94kH81bxYonUnz7b1qLxoZCKV0fzq6XTGAQXvg72HufpMwAoFguZAb5qTOv9FdNEdoZA8IUwIl"
PHONE_NUMBER_ID = "1303528422837098"

# ==========================================
# 2. FUNCIONES PARA ENVIAR MENSAJES
# ==========================================
def enviar_texto(numero_destino, texto):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": numero_destino,
        "type": "text",
        "text": {"body": texto}
    }
    respuesta = requests.post(url, headers=headers, json=data)
    print(f"🔍 [CHISMOSO TEXTO] Meta dice: {respuesta.text}")

def enviar_interactivo(numero_destino, texto, botones):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    
    lista_botones = []
    for i, btn_texto in enumerate(botones):
        lista_botones.append({
            "type": "reply",
            "reply": {
                "id": f"btn_{i}",
                "title": btn_texto
            }
        })

    data = {
        "messaging_product": "whatsapp",
        "to": numero_destino,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": texto},
            "action": {"buttons": lista_botones}
        }
    }
    respuesta = requests.post(url, headers=headers, json=data)
    print(f"🔍 [CHISMOSO BOTONES] Meta dice: {respuesta.text}")

# ==========================================
# 3. EL CEREBRO DEL BOT
# ==========================================
@app.route('/webhook', methods=['GET'])
def verificar_token():
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge'), 200
    return 'Error de autenticación', 403

@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    data = request.get_json()
    try:
        if 'entry' in data and 'changes' in data['entry'][0]:
            value = data['entry'][0]['changes'][0]['value']
            if 'messages' in value:
                mensaje_info = value['messages'][0]
                numero_cliente = mensaje_info['from']
                tipo_mensaje = mensaje_info['type']
                nombre_perfil = value['contacts'][0]['profile']['name']
                
                texto_recibido = ""
                if tipo_mensaje == 'button':
                    texto_recibido = mensaje_info['button']['text']
                elif tipo_mensaje == 'interactive':
                    texto_recibido = mensaje_info['interactive']['button_reply']['title']
                elif tipo_mensaje == 'text':
                    texto_recibido = mensaje_info['text']['body']
                
                print(f"\n📩 {nombre_perfil} respondió: '{texto_recibido}'")
                
                # --- RUTAS DE RESPUESTA ---
                # --- RUTAS DE RESPUESTA ---
                
                # 🟢 RUTA 1: Botón Positivo
                if texto_recibido == "SI LO CONSIDERO IMPORTANTE":
                    msg2 = f"¡Excelente visión, {nombre_perfil}!\n\nMás que un seminario tradicional, la Cumbre Millonarios Conscientes 2026 es una inmersión presencial. Actualmente tenemos la preventa activa. ¿Te comparto los formatos de entrada y precios?"
                    botones_m2 = ["Ver precios y promo", "Tengo dudas", "No continuar"]
                    enviar_interactivo(numero_cliente, msg2, botones_m2)

                # 🟢 RUTA 2: Muestra precios (Esta queda igual porque los botones los enviamos nosotros)
                elif texto_recibido == "Ver precios y promo":
                    msg3 = "¡Claro que sí! Aprovechando la preventa actual, estos son los valores:\n\n🎟️ General: $50 USD (2x1)\n🌟 VIP: $300 USD (2x1)\n💎 Platino: $1.200 USD (Individual)\n\n¿Qué formato se ajusta mejor?"
                    botones_m3 = ["Quiero comprar", "Cotizar empresa", "Tengo dudas"]
                    enviar_interactivo(numero_cliente, msg3, botones_m3)
                
                # 🔴 RUTA 3: Salida y rechazo (Agregamos tus dos botones negativos)
                elif texto_recibido in ["NO LO CONSIDERO IMPORTANTE", "NO ESTOY INTERESADO", "No continuar"]:
                    msg_salida = f"Entiendo perfectamente, {nombre_perfil}. El tiempo en la gerencia es limitado. No te escribiremos más sobre este evento.\n\nSi en el futuro buscas potenciar tu liderazgo a tu ritmo, te invito a seguirnos en Instagram con contenido gratuito para directivos:\n\n📱 @sigamed_john.camacho\n\n¡Muchísimo éxito con tus proyectos!"
                    enviar_texto(numero_cliente, msg_salida)
                    
    except Exception as e:
        print(f"❌ Error interno en Python: {e}")

    return 'EVENT_RECEIVED', 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)