from datetime import datetime
import json

class UserManagementService:
    def __init__(self, database):
        self.database = database

    def register_user(self, user_id, username):
        user_data = {
            "user_id": user_id,
            "username": username,
            "registered_at": datetime.now().isoformat(),
            "coupons": [],
            "files": []
        }
        self.database.save_user(user_data)

    def get_user(self, user_id):
        return self.database.get_user(user_id)

    def add_coupon_to_user(self, user_id, coupon_code):
        user = self.get_user(user_id)
        if user:
            user['coupons'].append(coupon_code)
            self.database.update_user(user_id, user)

    def add_file_to_user(self, user_id, file_info):
        user = self.get_user(user_id)
        if user:
            user['files'].append(file_info)
            self.database.update_user(user_id, user)

    def get_user_files(self, user_id):
        user = self.get_user(user_id)
        return user['files'] if user else []

    def get_user_coupons(self, user_id):
        user = self.get_user(user_id)
        return user['coupons'] if user else []