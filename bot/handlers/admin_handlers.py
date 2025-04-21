from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from services.file_upload_service import FileUploadService
from services.coupon_service import CouponService
from services.user_management_service import UserManagementService

file_upload_service = FileUploadService()
coupon_service = CouponService()
user_management_service = UserManagementService()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Admin Panel! Use /upload_file to upload files or /generate_coupon to create coupons.')

def upload_file(update: Update, context: CallbackContext) -> None:
    if context.args:
        file_path = context.args[0]
        result = file_upload_service.upload_file(file_path)
        update.message.reply_text(result)
    else:
        update.message.reply_text('Please provide a file path.')

def generate_coupon(update: Update, context: CallbackContext) -> None:
    coupon = coupon_service.generate_coupon()
    update.message.reply_text(f'Generated Coupon: {coupon}')

def list_users(update: Update, context: CallbackContext) -> None:
    users = user_management_service.get_all_users()
    update.message.reply_text('\n'.join(users))