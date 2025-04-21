from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
import os

UPLOAD_DIRECTORY = 'uploads/'

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('¡Bienvenido! 🎉 Puedes subir archivos aquí. 📂')

def upload_file(update: Update, context: CallbackContext) -> None:
    file = update.message.document.get_file()
    file_path = os.path.join(UPLOAD_DIRECTORY, update.message.document.file_name)
    file.download(file_path)
    update.message.reply_text(f'¡Archivo {update.message.document.file_name} subido con éxito! ✅')

def register_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document, upload_file))