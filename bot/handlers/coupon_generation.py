from datetime import datetime, timedelta
import random
import string

class Coupon:
    def __init__(self, code, expiration_date):
        self.code = code
        self.expiration_date = expiration_date
        self.redeemed = False

    def redeem(self):
        if not self.redeemed and datetime.now() < self.expiration_date:
            self.redeemed = True
            return True
        return False

class CouponGenerator:
    def __init__(self):
        self.coupons = []

    def generate_coupon(self, length=10, validity_days=30):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        expiration_date = datetime.now() + timedelta(days=validity_days)
        coupon = Coupon(code, expiration_date)
        self.coupons.append(coupon)
        return coupon

    def get_active_coupons(self):
        return [coupon for coupon in self.coupons if not coupon.redeemed and datetime.now() < coupon.expiration_date]

    def redeem_coupon(self, code):
        for coupon in self.coupons:
            if coupon.code == code:
                return coupon.redeem()
        return False