from aiogram import F,Router
from aiogram.types import Message
from keyboards.inline import products_inline
router=Router()

@router.message(lambda msg: msg.text == "Mahsulotlar")
async def show_products(message: Message, db):
    products = await db.get_products()
    await message.answer(
        "🛍 Mahsulotlar:",
        reply_markup=products_inline(products)
    )