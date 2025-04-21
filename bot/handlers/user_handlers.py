from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from bot.config import DATABASE_PATH, FILE_STORAGE_PATH
from bot.services.user_management_service import UserManagementService
from bot.services.coupon_service import CouponService
from bot.services.file_upload_service import FileUploadService

# Instancia del servicio con la base de datos
user_management_service = UserManagementService(database=DATABASE_PATH)

# Instancia del servicio de cupones
coupon_service = CouponService()

# Instancia del servicio de subida de archivos
file_upload_service = FileUploadService(upload_directory=FILE_STORAGE_PATH)

# Define tus handlers aquí
user_command_handlers = [
    # Agrega tus handlers de comandos aquí
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