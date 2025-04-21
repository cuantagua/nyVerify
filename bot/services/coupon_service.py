from datetime import datetime, timedelta
import random
import string

class Coupon:
    def __init__(self, code, expiration_date):
        self.code = code
        self.expiration_date = expiration_date
        self.redeemed = False

class CouponService:
    def __init__(self):
        self.coupons = []

    def generate_coupon(self, length=10, validity_days=30):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        expiration_date = datetime.now() + timedelta(days=validity_days)
        coupon = Coupon(code, expiration_date)
        self.coupons.append(coupon)
        return coupon

    def validate_coupon(self, code):
        for coupon in self.coupons:
            if coupon.code == code:
                if not coupon.redeemed and coupon.expiration_date > datetime.now():
                    return True
                break
        return False

    def redeem_coupon(self, code):
        for coupon in self.coupons:
            if coupon.code == code:
                if not coupon.redeemed and coupon.expiration_date > datetime.now():
                    coupon.redeemed = True
                    return True
                break
        return False

    def get_all_coupons(self):
        return self.coupons