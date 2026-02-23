from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

def users_inline(users):
    keyboard = []

    for user in users:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{user['name']} ({user['role']})",
                callback_data=f"user_{user['telegram_id']}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def role_inline(telegram_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👑 Admin",
                    callback_data=f"setrole_Admin_{telegram_id}"
                ),
                InlineKeyboardButton(
                    text="👤 User",
                    callback_data=f"setrole_user_{telegram_id}"
                )
            ]
        ]
    )


def products_inline(products):
    keyboard = []

    for product in products:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{product['name']} - {product['price']} so'm",
                callback_data=f"adminproduct_{product['id']}"
            )
        ])
        

    return InlineKeyboardMarkup(inline_keyboard=keyboard)