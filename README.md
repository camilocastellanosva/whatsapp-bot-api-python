# 🚀 WhatsApp Business API: Automated Prospecting & Follow-Up Engine

End-to-end automated lead prospecting and qualification system, integrated directly with the **Meta Graph API (WhatsApp Cloud API)**. 

It combines a batch-segmented broadcast engine with an asynchronous webhook receiver and a background watchdog for the automatic recovery of inactive prospects (remarketing/abandoned cart).

---

## 📌 Key Features

* **Ingestion & Sanitization Engine (Pandas):** Reads Excel (`.xlsx`) databases, normalizes international dialing codes (`+57`), cleans numeric formats, and parameterizes official Meta templates.
* **Interactive Decision Tree:** Real-time handling of interactive button responses (`quick_reply`, `interactive buttons`) to guide the user through the sales funnel.
* **Asynchronous Recovery Monitor (`threading`):** Tracks lead inactivity. If a user abandons the flow before completing an action, the system automatically triggers a scheduled reminder without blocking the main server.
* **Decoupled Architecture:** Clear separation between the outbound dispatcher (`motor_envios.py`) and the inbound event receiver (`bot_webhook.py`).

---

## 🏗️ Architecture Flow

```mermaid
graph TD
    A[Excel Database] -->|Pandas Ingest & Clean| B[Python Broadcast Engine]
    B -->|Meta Graph API| C[Client's WhatsApp]
    C -->|Interaction / Button Click| D[Flask Webhook]
    D -->|Payload Evaluation| E{Decision Tree}
    E -->|Immediate Response| C
    D -->|Logs Timestamp| F[Asynchronous Watchdog - Threads]
    F -->|Inactivity > 60 min| G[Follow-Up / Remarketing Message]
    G --> C
```



# 🚀 WhatsApp Business API: Automated Prospecting & Follow-Up Engine

Sistema automatizado de prospección y cualificación de leads de punta a punta, integrado directamente con la **Meta Graph API (WhatsApp Cloud API)**. 

Combina un motor de envíos segmentados por lotes con un receptor webhook asíncrono y un monitor en segundo plano (*Background Watchdog*) para la recuperación automática de prospectos inactivos (remarketing/carrito abandonado).

---

## 📌 Características Principales

* **Motor de Ingesta y Sanitización (Pandas):** Lee bases de datos en Excel (`.xlsx`), normaliza prefijos internacionales (`+57`), limpia formatos decimales y parametriza plantillas oficiales de Meta.
* **Árbol de Decisión Interactivo:** Manejo en tiempo real de respuestas de botones interactivos (`quick_reply`, `interactive buttons`) para guiar al usuario a través del embudo de ventas.
* **Monitor Asíncrono de Recuperación (`threading`):** Monitorea la inactividad del lead. Si un usuario abandona el flujo antes de completar la acción, el sistema dispara automáticamente un recordatorio programado sin bloquear el servidor.
* **Arquitectura Desacoplada:** Separación clara entre el despachador saliente (`motor_envios.py`) y el receptor de eventos entrantes (`bot_webhook.py`).

---

## 🏗️ Flujo de Arquitectura

```mermaid
graph TD
    A[Base de Datos Excel] -->|Pandas Ingest & Clean| B[Motor de Envíos Python]
    B -->|Meta Graph API| C[WhatsApp del Cliente]
    C -->|Interacción / Clic en Botón| D[Webhook Flask]
    D -->|Evaluación de Payload| E{Árbol de Decisiones}
    E -->|Respuesta Inmediata| C
    D -->|Registra Timestamp| F[Vigilante Asíncrono - Threads]
    F -->|Inactividad > 60 min| G[Mensaje de Seguimiento / Remarketing]
    G --> C
```


## 📸 Live Demo / Demostración Visual
<img width="848" height="332" alt="DEMO (8)" src="https://github.com/user-attachments/assets/c1652a9e-e034-44ef-8381-60446386ff77" />
<img width="495" height="243" alt="DEMO (7)" src="https://github.com/user-attachments/assets/eb6c749e-a869-4d96-a77b-9ea68b99e663" />
<img width="482" height="270" alt="DEMO (6)" src="https://github.com/user-attachments/assets/22bf676b-5e0d-4640-95ba-7bb778f28e6b" />
<img width="1216" height="477" alt="DEMO (5)" src="https://github.com/user-attachments/assets/9f3405e1-c570-4d5e-b276-1eaf81d5052a" />
<img width="1251" height="760" alt="DEMO (4)" src="https://github.com/user-attachments/assets/46a68f9a-746c-499e-8be2-56ad5ae1756b" />
<img width="502" height="507" alt="DEMO (3)" src="https://github.com/user-attachments/assets/5e4702b0-8d54-4eed-a2da-e1bd925e5dd2" />
<img width="483" height="552" alt="DEMO (2)" src="https://github.com/user-attachments/assets/0eedfc14-4c1d-49a6-9d54-253414b11b18" />
<img width="492" height="567" alt="DEMO (1)" src="https://github.com/user-attachments/assets/f4048118-79a3-4115-9b0b-35a4f44f3eeb" />

