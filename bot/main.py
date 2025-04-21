import sys
import os

# Añade el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from telegram.ext import Application
from bot.config import API_TOKEN
from bot.handlers.user_handlers import user_command_handlers
from bot.handlers.admin_handlers import admin_command_handlers

def main():
    # Crea la aplicación
    application = Application.builder().token(API_TOKEN).build()

    # Registra los handlers de usuario
    for handler in user_command_handlers:
        application.add_handler(handler)

    # Registra los handlers de administrador
    for handler in admin_command_handlers:
        application.add_handler(handler)

    # Inicia el bot
    application.run_polling()

if __name__ == '__main__':
    main()