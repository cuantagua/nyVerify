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

# Define tus handlers aquí
user_command_handlers = [
    MessageHandler(filters.Document.ALL, handle_file_upload),
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
        result = await coupon_service.redeem_coupon(coupon_code)
        await update.message.reply_text(f"🎟️ {result}")
    else:
        await update.message.reply_text("❌ Por favor, proporciona un código de cupón.")

async def mis_archivos(update: Update, context: CallbackContext) -> None:
    # Lógica para listar los archivos del usuario
    user_id = update.message.from_user.id
    files = await user_management_service.get_user_files(user_id)
    if files:
        await update.message.reply_text("📂 Tus archivos:\n" + "\n".join(files))
    else:
        await update.message.reply_text("📂 No tienes archivos subidos.")

# Lógica para manejar archivos enviados por el usuario
async def handle_file_upload(update: Update, context: CallbackContext) -> None:
    """Maneja la recepción de archivos enviados por el usuario."""
    document = update.message.document
    if document:
        file_id = document.file_id
        file_name = document.file_name

        # Guarda el file_id y el nombre del archivo en un archivo CSV
        with open(DATABASE_PATH, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([update.message.from_user.id, file_name, file_id])

        await update.message.reply_text(f"✅ Archivo recibido y almacenado: {file_name}")
    else:
        await update.message.reply_text("❌ No se pudo procesar el archivo. Por favor, inténtalo de nuevo.")