import requests
import config
import pandas as pd
import time

def enviar_plantilla(numero_destino, nombre_plantilla, variables=[]):
    url = f"https://graph.facebook.com/v17.0/{config.PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {config.TOKEN}", "Content-Type": "application/json"}
    
    componentes = []
    if variables:
        lista_parametros = [{"type": "text", "text": str(var)} for var in variables]
        componentes.append({"type": "body", "parameters": lista_parametros})

    data = {
        "messaging_product": "whatsapp",
        "to": numero_destino,
        "type": "template",
        "template": {
            "name": nombre_plantilla,
            "language": {"code": "es_CO"}, 
            "components": componentes
        }
    }
    
    try:
        respuesta = requests.post(url, headers=headers, json=data)
        if respuesta.status_code == 200:
            print(f"✅ Plantilla enviada a {numero_destino}")
        else:
            print(f"❌ Error enviando a {numero_destino}: {respuesta.json()}") 
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

FILA_INICIO = 0
FILA_FIN = 3  

def iniciar_campana():
    print(f"📊 Cargando Excel... Preparando lote desde la fila {FILA_INICIO} hasta la {FILA_FIN}")
    df = pd.read_excel('base_datos_leads.xlsx')
    
    lote_actual = df.iloc[FILA_INICIO:FILA_FIN]
    
    for index, fila in lote_actual.iterrows():
        numero_excel = str(fila['Teléfono']).replace('.0', '') 
        
        numero_cliente = f"57{numero_excel}" 
        
        nombre_cliente = str(fila['rep_legal'])
        empresa_cliente = str(fila['razon_social']) 
        
        variables = [nombre_cliente, empresa_cliente]
        
        enviar_plantilla(numero_cliente, "template_contacto1", variables)
        
        time.sleep(4) 

    print("🎉 ¡LOTE FINALIZADO! Ya puedes descansar o preparar el siguiente rango.")

iniciar_campana()