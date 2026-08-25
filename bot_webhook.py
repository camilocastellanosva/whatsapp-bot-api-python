from flask import Flask, request
import config
import requests
import threading
import time

app = Flask(__name__)


ultima_interaccion = {}

TIEMPO_ESPERA = 3600  

def monitor_seguimiento():
    """Este motor corre en silencio vigilando quién se quedó callado"""
    while True:
        tiempo_actual = time.time()
        
        for numero_cliente, tiempo_ultimo_mensaje in list(ultima_interaccion.items()):
            
            if (tiempo_actual - tiempo_ultimo_mensaje) > TIEMPO_ESPERA:
                print(f"⏰ ¡Alarma! {numero_cliente} se quedó callado. Disparando seguimiento...")
                
                texto_seguimiento = "Mensaje de prueba, por favor determinar el mensaje que va en esta sección."
                enviar_texto(numero_cliente, texto_seguimiento)
                
                del ultima_interaccion[numero_cliente]
                
        time.sleep(10) 

hilo_vigilante = threading.Thread(target=monitor_seguimiento, daemon=True)
hilo_vigilante.start()

@app.route('/webhook', methods=['GET'])
def verificar_token():
    token_recibido = request.args.get('hub.verify_token')
    if token_recibido == config.VERIFY_TOKEN:
        print("✅ Meta se conectó exitosamente al webhook.")
        return request.args.get('hub.challenge'), 200
    return 'Error de autenticación', 403

def enviar_texto(numero_destino, texto):
    url = f"https://graph.facebook.com/v17.0/{config.PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {config.TOKEN}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": numero_destino, "type": "text", "text": {"body": texto}}
    try:
        requests.post(url, headers=headers, json=data)
    except Exception as e:
        print(f"❌ Error texto: {e}")

def enviar_interactivo(numero_destino, texto_mensaje, lista_botones):
    url = f"https://graph.facebook.com/v17.0/{config.PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {config.TOKEN}", "Content-Type": "application/json"}
    botones_formateados = [{"type": "reply", "reply": {"id": btn, "title": btn}} for btn in lista_botones]
    data = {
        "messaging_product": "whatsapp", "to": numero_destino, "type": "interactive",
        "interactive": {"type": "button", "body": {"text": texto_mensaje}, "action": {"buttons": botones_formateados}}
    }
    try:
        requests.post(url, headers=headers, json=data)
    except Exception as e:
        print(f"❌ Error botones: {e}")

@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    data = request.get_json()
    try:
        entradas = data['entry'][0]['changes'][0]['value']
        
        if 'messages' in entradas:
            mensaje = entradas['messages'][0]
            numero_cliente = mensaje['from']
            
            ultima_interaccion[numero_cliente] = time.time()
            
            if mensaje['type'] == 'text':
                texto_recibido = mensaje['text']['body']
            elif mensaje['type'] in ['interactive', 'button']:
                if 'button_reply' in mensaje.get('interactive', {}):
                    texto_recibido = mensaje['interactive']['button_reply']['id']
                elif 'button' in mensaje:
                    texto_recibido = mensaje['button']['payload']
                else:
                    texto_recibido = "botón desconocido"
            else:
                texto_recibido = "Formato no soportado"

            print(f"📩 [{numero_cliente}] eligió: '{texto_recibido}'", flush=True)
            
            if texto_recibido in ["No me interesan", "En definitiva no", "No, gracias"]:
                despedida = (
                    "Entiendo.\n"
                    "Si en este momento tu desarrollo, el de tu empresa y tu equipo no son de tu interés, nuestra invitación no es para ti.\n\n"
                    "Sin embargo, si en algún momento quieres potencializar tu liderazgo personal o empresarial, Síguenos en Instagram y accede a herramientas gratuitas para personas y empresas de alto impacto.\n\n"
                    "📱 @sigamed_john.camacho\n"
                    "📱 @tu_conexion_holistica\n\n"
                    "¡Te deseo muchísimo éxito con tus proyectos!"
                )
                enviar_texto(numero_cliente, despedida)
                if numero_cliente in ultima_interaccion:
                    del ultima_interaccion[numero_cliente]

            elif texto_recibido == "No":
                persuasion = (
                    "Entiendo que quizás no veas la conexión ahora, pero Los resultados nacen de las decisiones y la energía tuyas y del equipo.\n\n"
                    "Si el liderazgo y el compromiso no fueran clave, ¿por qué las grandes empresas los priorizan? Pregúntate: ¿Qué es lo mejor que podrías lograr si lo intentas? y ¿Qué es lo que puedes perder si no?\n\n"
                    "Date el permiso de responderte honestamente esas preguntas, tomate el tiempo necesario.\n\n"
                    "Ahora, ¿Esto resuena contigo?"
                )
                enviar_interactivo(numero_cliente, persuasion, ["En definitiva no", "Tal vez"])

            elif texto_recibido in ["Si", "Tal vez"]:
                detalles = (
                    "El verdadero crecimiento ocurre cuando líder y equipo avanzan juntos, priorizando resultados y bienestar sostenido en el tiempo.\n\n"
                    "Quiero contarte sobre una experiencia presencial e inmersiva única, diseñada para transformar patrones mentales que frenan lo personal y afectan lo empresarial.\n\n"
                    "¿Te comparto más detalles?\n\n"
                    "Si tu mente ya dijo que no, confía y sigue en el proceso, conoce la información y te sorprenderás, al final, puedes tener material gratuito para ti y los tuyos."
                )
                enviar_interactivo(numero_cliente, detalles, ["No, gracias", "Si, quiero detalles"])

            elif texto_recibido == "Si, quiero detalles":
                info_cumbre = (
                    "Cumbre Millonarios Conscientes 2026 - Colombia\n\n"
                    "📅 Fecha: 29 y 30 de agosto de 2026.\n"
                    "📍 Ciudad: Medellín.\n"
                    "🏢 Lugar: City Hall El Rodeo.\n"
                    "⏰ Horario: 9:00 a. m. a 10:00 p. m. ambos días.\n"
                    "🎤 Speaker principal: Javi Rodríguez.\n"
                    "✨ Formato: 2 días presenciales, experiencia inmersiva.\n"
                    "🧠 Enfoque: PNL, coaching, identidad, mentalidad financiera y transformación personal.\n\n"
                    "No es: un curso, seminario o charla tradicional; es una experiencia vivencial e inmersiva."
                )
                enviar_interactivo(numero_cliente, info_cumbre, ["escuchar al Speaker", "Ver precios", "hablar con un asesor"])

            elif texto_recibido == "escuchar al Speaker":
                enviar_interactivo(numero_cliente, "Te ofrezco las siguientes opciones.", ["Acceder al Drive", "Acceder a Instagram", "Quiero comprar"])

            elif texto_recibido == "Acceder al Drive":
                texto_drive = "📁 Aquí tienes el material en Drive:\nhttps://acesse.one/ssf4aym\n\n¿Qué te gustaría hacer ahora?"
                enviar_interactivo(numero_cliente, texto_drive, ["Ver precios", "hablar con un asesor"])

            elif texto_recibido == "Acceder a Instagram":
                texto_ig = "📸 Conoce más en nuestras cuentas:\n@sigamed_john.camacho\n@tu_conexion_holistica\n\n¿Qué te gustaría hacer ahora?"
                enviar_interactivo(numero_cliente, texto_ig, ["Ver precios", "hablar con un asesor"])

            elif texto_recibido in ["Ver precios", "Quiero comprar"]:
                precios = (
                    "🎟️ Preventa actual\n\n"
                    "General: $50 USD — 2x1.\n"
                    "VIP: $300 USD — 2x1.\n"
                    "Platino: $1.200 USD — individual.\n\n"
                    "🔥 DESCUENTO A PARTIR DE 10 BOLETAS\n"
                    "El precio puede cambiar al siguiente lote sin fecha anunciada, por lo que comprar ahora asegura el precio disponible actualmente."
                )
                enviar_interactivo(numero_cliente, precios, ["Comprar de 1 a 9", "Comprar más de 10"])

            elif texto_recibido in ["hablar con un asesor", "Comprar de 1 a 9", "Comprar más de 10"]:
                asesor = "Claro que sí. Dinos por que medio quieres que te contactemos; Recomendamos el WhatsApp, para que tengas trazabilidad de la información."
                enviar_interactivo(numero_cliente, asesor, ["Video Llamada", "WhatsApp", "Telefono"])

            elif texto_recibido in ["Video Llamada", "WhatsApp", "Telefono"]:
                enviar_texto(numero_cliente, f"¡Perfecto! Un asesor se contactará contigo por {texto_recibido} a la brevedad posible.")
                # Apagamos el reloj cuando ya cerraron la solicitud
                if numero_cliente in ultima_interaccion:
                    del ultima_interaccion[numero_cliente]

    except Exception as e:
        pass
        
    return 'EVENT_RECEIVED', 200

if __name__ == '__main__':
    print("🤖 Recepcionista iniciado con SISTEMA DE SEGUIMIENTO. Esperando conexión...")
    app.run(port=5005, debug=True)