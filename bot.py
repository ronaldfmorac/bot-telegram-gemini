import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

# 1. CARGA Y VALIDACIÓN DE CONFIGURACIÓN
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("❌ Error: Faltan las llaves en el archivo .env")

# Configuración de Gemini (Usando el modelo más reciente de 2026)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3-flash') 

# Diccionario para guardar el historial por usuario (Memoria local temporal)
# En producción usarías una DB (Redis o MySQL), pero para portafolio esto es excelente
historiales = {}

# Logs profesionales
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2. LÓGICA DE IA CON MEMORIA
async def obtener_respuesta_ia(user_id, texto_usuario):
    """Mantiene una charla fluida usando el historial del usuario"""
    if user_id not in historiales:
        historiales[user_id] = model.start_chat(history=[])
    
    chat = historiales[user_id]
    try:
        response = chat.send_message(texto_usuario)
        return response.text
    except Exception as e:
        logger.error(f"Error en Gemini: {e}")
        return "⚠️ Lo siento, tuve un problema procesando tu mensaje. Intenta de nuevo."

# 3. FUNCIONES DEL BOT
async def inicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start personalizado"""
    user_name = update.effective_user.first_name
    # Limpiamos historial al reiniciar
    if update.effective_user.id in historiales:
        del historiales[update.effective_user.id]
        
    await update.message.reply_text(
        f"¡Hola {user_name}! 👋 Soy tu asistente inteligente.\n"
        "Puedo recordar lo que decimos en esta sesión. ¿En qué te ayudo hoy?"
    )

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja la comunicación, estados visuales y fragmentación"""
    user_id = update.effective_user.id
    texto_recibido = update.message.text

    # Efecto de "Escribiendo..." en Telegram
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)

    # Obtener respuesta de la IA
    respuesta_ia = await obtener_respuesta_ia(user_id, texto_recibido)
    
    # Fragmentación de mensajes (Límite de Telegram)
    LIMITE = 4000
    if len(respuesta_ia) <= LIMITE:
        await update.message.reply_text(respuesta_ia)
    else:
        for i in range(0, len(respuesta_ia), LIMITE):
            await update.message.reply_text(respuesta_ia[i:i + LIMITE])

# 4. ARRANQUE
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", inicio))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), manejar_mensaje))
    
    logger.info("🚀 Bot iniciado correctamente...")
    app.run_polling()