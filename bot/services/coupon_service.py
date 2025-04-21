from uuid import uuid4
import datetime

class CouponService:
    def __init__(self):
        self.coupons = {}

    def generate_coupon(self, user_id):
        coupon_code = str(uuid4())
        expiration_date = datetime.datetime.now() + datetime.timedelta(days=30)
        self.coupons[coupon_code] = {
            'user_id': user_id,
            'valid': True,
            'expiration_date': expiration_date
        }
        return coupon_code

    def redeem_coupon(self, coupon_code, user_id):
        if coupon_code in self.coupons:
            coupon = self.coupons[coupon_code]
            if coupon['valid'] and coupon['user_id'] == user_id:
                if datetime.datetime.now() < coupon['expiration_date']:
                    coupon['valid'] = False
                    return True  # Coupon redeemed successfully
                else:
                    return False  # Coupon expired
            else:
                return False  # Coupon invalid or not owned by user
        return False  # Coupon does not exist

    def check_coupon_status(self, coupon_code):
        if coupon_code in self.coupons:
            return self.coupons[coupon_code]
        return None  # Coupon does not exist