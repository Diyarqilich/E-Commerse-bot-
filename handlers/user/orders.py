from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "📦 Mening buyurtmalarim")
async def my_orders(message: Message):
    db = message.bot.dispatcher["db"]

    telegram_id = message.from_user.id
    user_id = await db.get_user_id(telegram_id)

    orders = await db.get_user_orders(user_id)

    if not orders:
        await message.answer("📭 Sizda hali buyurtmalar yo'q")
        return

    text = "📦 Sizning buyurtmalar tarixi:\n\n"
    for order in orders:
        text += (
            f"🆔 Buyurtma ID: {order['id']}\n"
            f"📊 Status: {order['order_status']}\n"
            f"💰 Jami: {order['total']} so'm\n\n"
        )

    await message.answer(text)