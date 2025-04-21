from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from bot.config import TOKEN
from bot.handlers.user_handlers import user_command_handlers
from bot.handlers.admin_handlers import admin_command_handlers

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register user command handlers
    for handler in user_command_handlers:
        dispatcher.add_handler(handler)

    # Register admin command handlers
    for handler in admin_command_handlers:
        dispatcher.add_handler(handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()