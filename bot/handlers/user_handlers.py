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

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to the Digital Content Store! Use /subir_archivo to upload files, /redimir_cupon to redeem coupons, and /mis_archivos to view your files.")

def subir_archivo(update: Update, context: CallbackContext) -> None:
    # Logic for handling file uploads
    update.message.reply_text("Please send the file you want to upload.")

def redimir_cupon(update: Update, context: CallbackContext) -> None:
    # Logic for redeeming coupons
    coupon_code = context.args[0] if context.args else None
    if coupon_code:
        result = coupon_service.redeem_coupon(coupon_code)
        update.message.reply_text(result)
    else:
        update.message.reply_text("Please provide a coupon code.")

def mis_archivos(update: Update, context: CallbackContext) -> None:
    # Logic for listing user's files
    user_id = update.message.from_user.id
    files = user_management_service.get_user_files(user_id)
    if files:
        update.message.reply_text("Your files:\n" + "\n".join(files))
    else:
        update.message.reply_text("You have no uploaded files.")