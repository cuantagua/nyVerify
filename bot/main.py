import sys
import os

# Añade el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from telegram.ext import Application, CommandHandler
from bot.config import API_TOKEN
from bot.handlers.user_handlers import user_command_handlers
from bot.handlers.admin_handlers import admin_command_handlers

def start(update, context):
    """Muestra las opciones disponibles al usuario."""
    options = (
        "👋 ¡Hola! Estas son las opciones disponibles:\n"
        "/subir_archivo - Subir un archivo\n"
        "/redimir_cupon - Redimir un cupón\n"
        "/mis_archivos - Ver tus archivos\n"
        "/comprar - Comprar más cupones\n"
    )
    update.message.reply_text(options)

def main():
    # Crea la aplicación
    application = Application.builder().token(API_TOKEN).build()

    # Agrega el comando /start
    application.add_handler(CommandHandler("start", start))

    # Registra los handlers de usuario
    for handler in user_command_handlers:
        application.add_handler(handler)

    # Registra los handlers de administrador
    for handler in admin_command_handlers:
        application.add_handler(handler)

    # Mensaje en consola para indicar que el bot está encendido
    print("✅ El bot está encendido y funcionando...")

    # Inicia el bot
    application.run_polling()

if __name__ == '__main__':
    main()