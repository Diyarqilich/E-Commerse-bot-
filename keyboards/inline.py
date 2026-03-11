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

def inline_action(product_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Edit",callback_data=f"edit_product_{product_id}"),InlineKeyboardButton(text="Delete",callback_data=f"delete_product_{product_id}")]
        ]
    )

def cart_keyboard(products):

    keyboard = []

    for product in products:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{product['name']} - {product['price']} so'm",
                callback_data=f"product_{product['id']}"
            ),
            InlineKeyboardButton(
                text="❌",
                callback_data=f"remove_{product['id']}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            text="✅ Buyurtma berish",
            callback_data="checkout"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def payment_keyboard():

    keyboard = [
        [
            InlineKeyboardButton(
                text="💳 Karta orqali to'lov",
                callback_data="pay_card"
            )
        ],
        [
            InlineKeyboardButton(
                text="💵 Naqd to'lov",
                callback_data="pay_cash"
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)