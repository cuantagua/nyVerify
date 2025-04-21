# Telegram Digital Sales Bot

This project is a Telegram bot designed to manage the sale of digital content. It includes features for file uploads, unique coupon generation, and user management.

## Features

- **File Uploads**: Users can upload digital files, which are stored and managed by the bot.
- **Coupon Generation**: The bot generates unique coupons for users, which can be redeemed for discounts or access to content.
- **User Management**: The bot tracks user registrations, manages access control, and keeps records of user-specific files and coupons.

## Project Structure

```
telegram-digital-sales-bot
├── bot
│   ├── __init__.py
│   ├── main.py
│   ├── handlers
│   │   ├── __init__.py
│   │   ├── user_handlers.py
│   │   └── admin_handlers.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── file_upload_service.py
│   │   ├── coupon_service.py
│   │   └── user_management_service.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── helpers.py
│   └── config.py
├── requirements.txt
├── .env
└── README.md
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd telegram-digital-sales-bot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your API keys and other sensitive information.

4. Run the bot:
   ```
   python bot/main.py
   ```

## Usage Guidelines

- Users can interact with the bot using commands such as `/subir_archivo`, `/redimir_cupon`, and `/mis_archivos`.
- Admins have access to additional commands for managing files and generating coupons.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.