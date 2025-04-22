from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, filters
from bot.config import DATABASE_PATH, FILE_STORAGE_PATH
from bot.services.user_management_service import UserManagementService
from bot.services.coupon_service import CouponService
from bot.services.file_upload_service import FileUploadService
import os
import csv

# Instancia del servicio con la base de datos
user_management_service = UserManagementService(database=DATABASE_PATH)

# Instancia del servicio de cupones
coupon_service = CouponService()

# Instancia del servicio de subida de archivos
file_upload_service = FileUploadService(upload_directory=FILE_STORAGE_PATH)

# Lógica para manejar archivos enviados por el usuario
async def handle_file_upload(update: Update, context: CallbackContext) -> None:
    """Maneja la recepción de archivos enviados por el usuario."""
    document = update.message.document
    audio = update.message.audio
    video = update.message.video
    voice = update.message.voice

    # Verifica si el mensaje contiene un archivo reenviado
    if update.message.forward_date:
        await update.message.reply_text("⚠️ Este archivo fue reenviado. Asegúrate de enviar el archivo original.")
        return

    # Procesa documentos
    if document:
        file_id = document.file_id
        file_name = document.file_name
        file_type = "Documento"

    # Procesa audios
    elif audio:
        file_id = audio.file_id
        file_name = audio.file_name or "audio.mp3"
        file_type = "Audio"

    # Procesa videos
    elif video:
        file_id = video.file_id
        file_name = video.file_name or "video.mp4"
        file_type = "Video"

    # Procesa mensajes de voz
    elif voice:
        file_id = voice.file_id
        file_name = "voice.ogg"
        file_type = "Mensaje de voz"

    else:
        await update.message.reply_text("❌ No se pudo procesar el archivo. Por favor, inténtalo de nuevo.")
        return

    # Guarda el file_id y el nombre del archivo en un archivo CSV
    with open(DATABASE_PATH, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([update.message.from_user.id, file_name, file_id, file_type])

    await update.message.reply_text(f"✅ Archivo recibido y almacenado: {file_name} ({file_type})")

# Define tus handlers aquí
user_command_handlers = [
    # Handler para documentos
    MessageHandler(filters.Document, handle_file_upload),
    # Handler para audios
    MessageHandler(filters.Audio, handle_file_upload),
    # Handler para videos
    MessageHandler(filters.Video, handle_file_upload),
    # Handler para mensajes de voz
    MessageHandler(filters.Voice, handle_file_upload),
]

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "👋 ¡Bienvenido a la Tienda de Contenidos Digitales! Usa /subir_archivo para subir archivos, /redimir_cupon para redimir cupones y /mis_archivos para ver tus archivos."
    )

async def subir_archivo(update: Update, context: CallbackContext) -> None:
    # Lógica para manejar la subida de archivos
    await update.message.reply_text("📤 Por favor, envía el archivo que deseas subir.")

async def redimir_cupon(update: Update, context: CallbackContext) -> None:
    # Lógica para redimir cupones
    coupon_code = context.args[0] if context.args else None
    if coupon_code:
        result = "Cupón redimido correctamente."  # Simula la lógica de redimir cupones
        await update.message.reply_text(f"🎟️ {result}")
    else:
        await update.message.reply_text("❌ Por favor, proporciona un código de cupón.")

async def mis_archivos(update: Update, context: CallbackContext) -> None:
    # Lógica para listar los archivos del usuario
    user_id = update.message.from_user.id
    files = ["archivo1.pdf", "archivo2.mp3"]  # Simula la lógica de obtener archivos
    if files:
        await update.message.reply_text("📂 Tus archivos:\n" + "\n".join(files))
    else:
        await update.message.reply_text("📂 No tienes archivos subidos.")