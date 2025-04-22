from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, filters, ConversationHandler
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

# Estados para el flujo de conversación
ASK_GENERATE_CODES, ASK_CODE_QUANTITY = range(2)

# Define tus handlers aquí
user_command_handlers = [
    # Ejemplo de un handler para manejar archivos adjuntos
    MessageHandler(filters.ATTACHMENT, handle_file_upload),
    # Otros handlers pueden ser agregados aquí
]

# Lógica para manejar archivos enviados por el usuario
async def handle_file_upload(update: Update, context: CallbackContext) -> int:
    """Maneja la recepción de archivos enviados por el usuario."""
    document = update.message.document
    audio = update.message.audio
    video = update.message.video
    voice = update.message.voice

    # Verifica si el mensaje contiene un archivo reenviado
    if hasattr(update.message, "forward_date") and update.message.forward_date:
        await update.message.reply_text("⚠️ Este archivo fue reenviado. Asegúrate de enviar el archivo original.")
        return ConversationHandler.END

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
        return ConversationHandler.END

    # Guarda el file_id y el nombre del archivo en un archivo CSV
    with open(DATABASE_PATH, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([update.message.from_user.id, file_name, file_id, file_type])

    # Guarda el archivo en el contexto para usarlo más adelante
    context.user_data["file_name"] = file_name
    context.user_data["file_type"] = file_type

    await update.message.reply_text(f"✅ Archivo recibido y almacenado: {file_name} ({file_type})")

    # Pregunta si desea generar códigos
    reply_keyboard = [["Sí", "No"]]
    await update.message.reply_text(
        "¿Deseas generar códigos para este archivo?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return ASK_GENERATE_CODES

async def ask_code_quantity(update: Update, context: CallbackContext) -> int:
    """Pregunta cuántos códigos desea generar."""
    user_response = update.message.text
    if user_response.lower() == "sí":
        await update.message.reply_text("¿Cuántos códigos deseas generar?")
        return ASK_CODE_QUANTITY
    else:
        await update.message.reply_text("✅ Proceso finalizado. No se generarán códigos.")
        return ConversationHandler.END

async def generate_codes(update: Update, context: CallbackContext) -> int:
    """Genera los códigos solicitados."""
    try:
        quantity = int(update.message.text)
        file_name = context.user_data.get("file_name")
        file_type = context.user_data.get("file_type")

        # Simula la generación de códigos
        codes = [f"{file_name}_CODE_{i+1}" for i in range(quantity)]

        # Responde con los códigos generados
        await update.message.reply_text(
            f"✅ Se generaron {quantity} códigos para el archivo '{file_name}':\n" + "\n".join(codes)
        )
    except ValueError:
        await update.message.reply_text("❌ Por favor, ingresa un número válido.")
        return ASK_CODE_QUANTITY

    return ConversationHandler.END

# Define el flujo de conversación para la subida de archivos
file_upload_conversation = ConversationHandler(
    entry_points=[MessageHandler(filters.ATTACHMENT, handle_file_upload)],
    states={
        ASK_GENERATE_CODES: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_code_quantity)],
        ASK_CODE_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, generate_codes)],
    },
    fallbacks=[],
)

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
