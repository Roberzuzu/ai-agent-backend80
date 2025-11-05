import os
import logging
import asyncio
from telegram import Update, InputFile
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ContextTypes, filters
)
import aiohttp
import motor.motor_asyncio
# Import CerebroAI from parent directory
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from agent_core import CerebroAI
from datetime import datetime

# ===== CONFIG: Variables from environment/Render =====
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CEREBRO_API = os.environ.get("CEREBRO_API", "https://ai-agent-backend80.onrender.com/api")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://ai-agent-backend80.onrender.com")
PORT = int(os.environ.get("PORT", 10000))

# MongoDB connection
MONGO_URL = os.environ.get("MONGO_URL", "")
if MONGO_URL:
    mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    db = mongo_client.get_database("cerebro_db")
else:
    # Simple in-memory fallback if no MongoDB
    db = None

# Initialize CerebroAI (use empty admin_id for now)
cerebro_ai = None
if db is not None:
    cerebro_ai = CerebroAI(db=db, admin_id="telegram_bot")

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== COMMANDS ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧠 Hola, soy CEREBRO - tu asistente ejecutivo.\n\n"
        "Puedo ayudarte con gestión, análisis, monetización y mucho más.\n\n"
        "Simplemente escríbeme o envíame archivos."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Escribe cualquier pregunta o envía archivos/fotos/videos.\n"
        "/start para saludar\n"
        "/ayuda para ayuda general."
    )

# ========== MESSAGES AND FILES ==========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text:
        await process_user_query(update, text)
    elif update.message.document or update.message.photo or update.message.video:
        await handle_file(update)
    else:
        await update.message.reply_text("No entiendo el mensaje, envía texto o un archivo válido.")

async def handle_file(update: Update):
    file_info = None
    file_name = "file"
    
    if update.message.document:
        file_info = update.message.document
        file_name = file_info.file_name or "documento"
    elif update.message.photo:
        file_info = update.message.photo[-1]
        file_name = f"foto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    elif update.message.video:
        file_info = update.message.video
        file_name = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    else:
        await update.message.reply_text("No pude reconocer el tipo de archivo enviado.")
        return
    
    file = await file_info.get_file()
    file_path = f"/tmp/{file_name}"
    await file.download_to_drive(file_path)
    
    await update.message.reply_text("📤 Archivo recibido. Procesando...")
    response_text = await send_file_to_backend(file_path, file_name)
    os.remove(file_path)
    await update.message.reply_text(response_text)

async def send_file_to_backend(path, file_name):
    url = f"{CEREBRO_API}/upload"
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
            with open(path, "rb") as f:
                data = aiohttp.FormData()
                data.add_field('file', f, filename=file_name)
                async with session.post(url, data=data) as resp:
                    if resp.status == 200:
                        j = await resp.json()
                        link = j.get("file_url") or j.get("link")
                        summary = j.get("summary", "Archivo procesado correctamente.")
                        return f"{summary}\n\n{link}" if link else summary
                    else:
                        return "El backend no pudo procesar el archivo. Intenta de nuevo más tarde."
    except Exception as e:
        return f"Error procesando archivo: {str(e)}"

async def process_user_query(update: Update, text: str):
    """Process user query using CerebroAI directly"""
    if not cerebro_ai:
        await update.message.reply_text(
            "❌ No se pudo inicializar el agente AI. Verifica la configuración de MONGO_URL y las API keys."
        )
        return
    
    try:
        user_id = str(update.message.from_user.id)
        
        # Use CerebroAI to process the command
        result = await cerebro_ai.procesar_comando(
            command=text,
            user_id=user_id,
            conversation_history=None  # Let CerebroAI load from DB
        )
        
        if result.get('success'):
            response = result.get('response', 'Sin respuesta del agente.')
            # Send response (truncate if too long for Telegram)
            await update.message.reply_text(response[:4096])
        else:
            error_msg = result.get('response', 'Error procesando tu solicitud.')
            await update.message.reply_text(f"⚠️ {error_msg}")
            
    except Exception as e:
        logger.error(f"Error en process_user_query: {str(e)}", exc_info=True)
        await update.message.reply_text(
            f"❌ Error procesando tu mensaje: {str(e)[:200]}\n\n"
            "Por favor intenta de nuevo o contacta al administrador."
        )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update error: {context.error}")

# ===== WEBHOOK STARTUP FOR RENDER / LOCAL POLLING =====
 def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ayuda", help_command))
    application.add_handler(MessageHandler(filters.ALL, handle_message))
    application.add_error_handler(error_handler)
    
    # Always use polling since we're integrated with FastAPI
    logger.info("🤖 Starting Telegram Bot in POLLING mode")
    application.run_polling()
