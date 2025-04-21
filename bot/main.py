from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from handlers.file_upload import handle_file_upload
from handlers.coupon_generation import generate_coupon
from handlers.user_management import register_user, get_user_info
import logging
import config

# Configuración del registro de logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def inicio(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('🎉 ¡Bienvenido al Bot de Venta de Contenido Digital!')

def principal() -> None:
    # Crear el Updater y pasarle el token del bot.
    updater = Updater(config.BOT_TOKEN)

    # Obtener el dispatcher para registrar los manejadores
    dispatcher = updater.dispatcher

    # Registrar manejadores de comandos
    dispatcher.add_handler(CommandHandler("inicio", inicio))
    dispatcher.add_handler(CommandHandler("registrar", register_user))
    dispatcher.add_handler(CommandHandler("cupon", generate_coupon))
    
    # Registrar manejador de mensajes para la subida de archivos
    dispatcher.add_handler(MessageHandler(Filters.document, handle_file_upload))

    # Iniciar el bot
    updater.start_polling()

    # Ejecutar el bot hasta que se envíe una señal para detenerlo
    updater.idle()

if __name__ == '__main__':
    principal()