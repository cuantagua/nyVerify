from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from bot.config import FILE_STORAGE_PATH, DATABASE_PATH
from bot.services.file_upload_service import FileUploadService
from bot.services.coupon_service import CouponService
from bot.services.user_management_service import UserManagementService
from telegram.ext import ContextTypes

# Instancia del servicio de subida de archivos
file_upload_service = FileUploadService(upload_directory=FILE_STORAGE_PATH)

# Instancia del servicio de cupones
coupon_service = CouponService()

# Instancia del servicio de gestión de usuarios
user_management_service = UserManagementService(database=DATABASE_PATH)

# Define tus handlers aquí
admin_command_handlers = [
    # Agrega tus handlers de comandos aquí
]
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('👋 ¡Bienvenido al Panel de Administración! Usa /upload_file para subir archivos o /generate_coupon para crear cupones.')

async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        file_path = context.args[0]
        result = await file_upload_service.upload_file(file_path)
        await update.message.reply_text(f'📂 Resultado de la subida: {result}')
    else:
        await update.message.reply_text('⚠️ Por favor, proporciona una ruta de archivo.')

async def generate_coupon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    coupon = await coupon_service.generate_coupon()
    await update.message.reply_text(f'🎟️ Cupón generado: {coupon}')

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    users = await user_management_service.get_all_users()
    if users:
        await update.message.reply_text(f'👥 Lista de usuarios:\n' + '\n'.join(users))
    else:
        await update.message.reply_text('⚠️ No hay usuarios registrados.')
