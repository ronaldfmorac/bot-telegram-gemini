# 🤖 Telegram AI Bot con Gemini 3 Flash

Este es un bot de Telegram inteligente desarrollado en Python que utiliza la API de Google Gemini para responder consultas en tiempo real. Soporta respuestas largas mediante fragmentación automática de mensajes.

## 🚀 Características
- **IA de última generación:** Integración con Gemini 3 Flash.
- **Asincronismo:** Construido con `python-telegram-bot` para manejar múltiples usuarios.
- **Manejo de errores:** Sistema de fragmentación para mensajes que superan los 4096 caracteres.
- **Seguridad:** Uso de variables de entorno para protección de credenciales.

## 🛠️ Instalación y Configuración

Sigue estos pasos para tener tu propio bot funcionando:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
cd tu-repositorio

### 2. Crear un entorno virtual
python -m venv venv
# Activar en Windows:
.\venv\Scripts\activate
# Activar en Mac/Linux:
source venv/bin/activate

### 3. Instalar dependencias
pip install -r requirements.txt

### 4. Configurar credenciales
Crea un archivo .env en la carpeta raíz y añade tus llaves:

TELEGRAM_TOKEN=TU_TOKEN_DE_BOTFATHER
GEMINI_API_KEY=TU_API_KEY_DE_GOOGLE_STUDIO

### 5. Ejecutar el bot
python bot.py

Tecnologías utilizadas
Python 3.14+

FastAPI (opcional para webhooks)

Google Generative AI SDK

Python Telegram Bot Library

Desarrollado por Ronald Mora - Ingeniero de Sistemas.