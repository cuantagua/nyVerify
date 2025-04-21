def format_coupon(coupon_code):
    return f"Your coupon code is: {coupon_code}"

def send_message(bot, chat_id, message):
    bot.send_message(chat_id, message)

def validate_coupon(coupon_code, valid_coupons):
    return coupon_code in valid_coupons

def log_action(user_id, action):
    with open('action_log.txt', 'a') as log_file:
        log_file.write(f"User {user_id} performed action: {action}\n")