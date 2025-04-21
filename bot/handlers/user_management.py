from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
from bot.services.user_service import UserService

user_service = UserService()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('¡Bienvenido! 👋 Usa /register para crear una cuenta. 📝')

def register(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    if user_service.register_user(user_id, username):
        update.message.reply_text('¡Registro exitoso! ✅')
    else:
        update.message.reply_text('Ya estás registrado. 🔒')

def user_info(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_data = user_service.get_user_data(user_id)

    if user_data:
        update.message.reply_text(f'ID de usuario: {user_data["id"]} 🆔\nNombre de usuario: {user_data["username"]} 👤')
    else:
        update.message.reply_text('Usuario no encontrado. ❌ Por favor, regístrate primero. 📝')

def set_permissions(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    permissions = context.args

    if user_service.set_user_permissions(user_id, permissions):
        update.message.reply_text('Permisos actualizados con éxito. ✅')
    else:
        update.message.reply_text('No se pudieron actualizar los permisos. ❌')

def handle_unknown(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Lo siento, no entendí ese comando. 🤔')