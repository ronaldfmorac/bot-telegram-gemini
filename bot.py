import os
from dotenv import load_dotenv
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

load_dotenv()
# 1. CONFIGURACIÓN DE APIS (Usa tus llaves aquí)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configuramos Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3-flash-preview')
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"Modelo disponible: {m.name}")

# Configuración de logs (para ver errores en la consola)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 2. LÓGICA DE LA IA
async def obtener_respuesta_ia(texto_usuario):
    """Envía el texto a Gemini y devuelve la respuesta"""
    try:
        response = model.generate_content(texto_usuario)
        return response.text
    except Exception as e:
        return f"Error con la IA: {str(e)}"

# 3. FUNCIONES DEL BOT
async def inicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde al comando /start"""
    await update.message.reply_text("¡Hola Fabián! Soy tu asistente con IA. Pregúntame lo que quieras.")

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recibe el texto, lo pasa a la IA y fragmenta la respuesta si es muy larga"""
    texto_recibido = update.message.text
    
    # 1. Obtenemos la respuesta de Gemini
    respuesta_ia = await obtener_respuesta_ia(texto_recibido)
    
    # 2. Definimos el límite de Telegram (usamos 4000 para estar seguros)
    LIMITE = 4000

    # 3. Si la respuesta es corta, se envía normal
    if len(respuesta_ia) <= LIMITE:
        await update.message.reply_text(respuesta_ia)
    else:
        # 4. Si es muy larga, la cortamos en trozos y enviamos varios mensajes
        for i in range(0, len(respuesta_ia), LIMITE):
            pedazo = respuesta_ia[i:i + LIMITE]
            await update.message.reply_text(pedazo)

# 4. ARRANQUE DEL SERVIDOR
if __name__ == '__main__':
    # Creamos la aplicación del bot
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Comandos
    app.add_handler(CommandHandler("start", inicio))
    
    # Mensajes de texto (Filtramos para que solo lea texto, no fotos/audios)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), manejar_mensaje))
    
    print("Bot encendido... Presiona Ctrl+C para apagarlo")
    app.run_polling()