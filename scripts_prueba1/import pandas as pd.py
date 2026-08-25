import pandas as pd
import requests
import time
from datetime import datetime

# ==========================================
# 1. CREDENCIALES DE META
# ==========================================
TOKEN = "3HurCuhTJQPJGttb5P3Hhb9LINV_jnRHF3ctjGxPYp1i4oQ9"
PHONE_NUMBER_ID = "1303528422837098"

# ==========================================
# 2. CONFIGURACIÓN DE ESTRATEGIA (ANTI-SPAM)
# ==========================================
# Cambia este número al iniciar tu día de trabajo: 1 para el primer día, 2 para el segundo, etc.
DIA_DE_CAMPANA = 1 

# Diccionario de calentamiento: Define cuántos enviar en total según el día
LIMITES_DIARIOS = {
    1: 50,   # Día 1: 50 mensajes en total
    2: 100,  # Día 2: 100 mensajes en total
    3: 150,
    4: 250,
    5: 400
}

LOTE_MAXIMO = 25 
TIEMPO_ESPERA_HORAS = 2 

def enviar_plantilla(numero_destino, nombre_cliente, nombre_empresa):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": str(numero_destino),
        "type": "template",
        "template": {
            "name": "prueba_botones_sigamed", 
            "language": {
                "code": "es"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": nombre_cliente}, # Variable {{1}}
                        {"type": "text", "text": nombre_empresa}  # Variable {{2}}
                    ]
                }
            ]
        }
    }
    
    respuesta = requests.post(url, headers=headers, json=data)
    if respuesta.status_code == 200:
        return "Enviado"
    else:
        error_data = respuesta.json()
        
        if 'error' in error_data and 'message' in error_data['error']:
            mensaje_error = error_data['error']['message']
            
            if "not on WhatsApp" in mensaje_error or "invalid phone number" in mensaje_error:
                return "Sin WhatsApp"
                
        return "Error General"


def ejecutar_campana():
    print(f"🚀 Iniciando campaña - DÍA {DIA_DE_CAMPANA}")
    limite_hoy = LIMITES_DIARIOS.get(DIA_DE_CAMPANA, 50)
    print(f"🎯 Límite total para hoy: {limite_hoy} mensajes.")
    
    # Leer el Excel
    archivo_excel = 'base_datos_leads.xlsx'
    try:
        df = pd.read_excel(archivo_excel)
    except Exception as e:
        print(f"❌ Error al leer el Excel: {e}")
        return

    # Filtrar los que no han sido contactados
    pendientes = df[df['Estado'].isnull() | (df['Estado'] == '')]
    
    if pendientes.empty:
        print("✅ No hay contactos pendientes en la base de datos.")
        return

    # Tomar solo la cantidad permitida para hoy
    contactos_hoy = pendientes.head(limite_hoy)
    total_a_enviar = len(contactos_hoy)
    print(f"📊 Se encontraron {total_a_enviar} contactos pendientes para la cuota de hoy.")

    mensajes_enviados_hoy = 0

    # Iterar sobre los contactos de hoy
    for index, row in contactos_hoy.iterrows():
        # Verificamos si es momento de hacer la pausa de 2 horas
        if mensajes_enviados_hoy > 0 and mensajes_enviados_hoy % LOTE_MAXIMO == 0:
            print(f"\n⏳ Lote de {LOTE_MAXIMO} completado.")
            print(f"💤 Pausando envíos por {TIEMPO_ESPERA_HORAS} horas para proteger el número...")
            # Convertimos las horas a segundos para el sleep
            time.sleep(TIEMPO_ESPERA_HORAS * 3600) 
            print("\n⏰ ¡Pausa terminada! Reanudando envíos...")

        numero = row['Telefono']
        nombre = row['Nombre']
        empresa = row['Empresa']
        
        print(f"➡️ Enviando a: {nombre} de {empresa} ({numero})...")
        
        # Intentar enviar el mensaje
        exito = enviar_plantilla(numero, nombre, empresa)
        
        if resultado == "Enviado":
            df.at[index, 'Estado'] = 'Enviado'
            print("   ✅ Éxito")
            # Solo sumamos al contador de hoy si efectivamente se envió
            mensajes_enviados_hoy += 1 
            time.sleep(3) # Pausa humana solo si el mensaje salió
            
        elif resultado == "Sin WhatsApp":
            df.at[index, 'Estado'] = 'Sin WhatsApp (Línea Fija o Inactiva)'
            print("   ⏭️ Saltando (No tiene WhatsApp)")
            # No sumamos al contador ni pausamos, para que limpie la base rápido
            
        else:
            df.at[index, 'Estado'] = 'Error'
            print("   ❌ Falló por otra razón")
            # Tampoco sumamos al contador porque rebotó
            
        # 3. Guardamos la fecha y el archivo
        df.at[index, 'Fecha_Envio'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df.to_excel(archivo_excel, index=False)
        
    # -------- FIN DEL CICLO FOR --------

    print(f"\n🎉 ¡Campaña de hoy finalizada! Se enviaron con éxito {mensajes_enviados_hoy} mensajes.")

if __name__ == "__main__":
    ejecutar_campana()