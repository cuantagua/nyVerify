from telegram import Update
from telegram.ext import ContextTypes
import os

class FileUploadService:
    def __init__(self, upload_directory):
        self.upload_directory = upload_directory
        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory)

    async def handle_file_upload(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        file = update.message.document

        if file:
            file_path = os.path.join(self.upload_directory, file.file_name)
            await file.get_file().download(file_path)
            await update.message.reply_text(f"File '{file.file_name}' uploaded successfully!")
        else:
            await update.message.reply_text("No file found to upload.")