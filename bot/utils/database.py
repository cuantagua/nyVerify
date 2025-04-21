import pandas as pd
import os

class Database:
    def __init__(self, user_file='users.csv', coupon_file='coupons.csv'):
        self.user_file = user_file
        self.coupon_file = coupon_file
        self.ensure_files_exist()

    def ensure_files_exist(self):
        if not os.path.isfile(self.user_file):
            pd.DataFrame(columns=['user_id', 'username', 'files']).to_csv(self.user_file, index=False)
        if not os.path.isfile(self.coupon_file):
            pd.DataFrame(columns=['coupon_code', 'is_redeemed']).to_csv(self.coupon_file, index=False)

    def add_user(self, user_id, username):
        df = pd.read_csv(self.user_file)
        if not df[df['user_id'] == user_id].empty:
            return False
        df = df.append({'user_id': user_id, 'username': username, 'files': ''}, ignore_index=True)
        df.to_csv(self.user_file, index=False)
        return True

    def get_user(self, user_id):
        df = pd.read_csv(self.user_file)
        user = df[df['user_id'] == user_id]
        return user.to_dict(orient='records')[0] if not user.empty else None

    def add_coupon(self, coupon_code):
        df = pd.read_csv(self.coupon_file)
        if not df[df['coupon_code'] == coupon_code].empty:
            return False
        df = df.append({'coupon_code': coupon_code, 'is_redeemed': False}, ignore_index=True)
        df.to_csv(self.coupon_file, index=False)
        return True

    def redeem_coupon(self, coupon_code):
        df = pd.read_csv(self.coupon_file)
        if df[df['coupon_code'] == coupon_code].empty:
            return False
        df.loc[df['coupon_code'] == coupon_code, 'is_redeemed'] = True
        df.to_csv(self.coupon_file, index=False)
        return True

    def get_all_coupons(self):
        df = pd.read_csv(self.coupon_file)
        return df.to_dict(orient='records')