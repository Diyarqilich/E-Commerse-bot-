from aiogram import F,Router
from aiogram.types import Message,CallbackQuery
from keyboards.inline import products_inline,cart_keyboard,payment_keyboard
from filters.filter import RoleFilter

router=Router()

@router.message(F.text == "Mahsulotlar")
async def show_products(message: Message, db):
    product = await db.get_products()
    await message.answer(
        "🛍 Mahsulotlar:",
        reply_markup=products_inline(product)
    )

@router.callback_query(F.data.startswith("adminproduct_"),RoleFilter("user"))
async def add_to_cart(call: CallbackQuery,db):

    product_id = int(call.data.split("_")[1])
    user_id = await db.get_user_id(call.from_user.id)

    await db.add_product_to_cart(int(user_id), product_id)

    await call.answer("Mahsulot savatchaga qo'shildi 🛒")

@router.message(F.text == "🛒 Savatcha",RoleFilter("user"))
async def show_cart(message: Message,db):
    user_id = await db.get_user_id(message.from_user.id)
    products = await db.get_cart_products(user_id)

    if not products:
        await message.answer("Savatcha bo'sh")
        return

    await message.answer(
        "Savatchangiz:",
        reply_markup=cart_keyboard(products)
    )

@router.callback_query(F.data.startswith("remove_"))
async def rm_product(call:CallbackQuery,db):
    product_id=int(call.data.split("_")[1])
    user_id = await db.get_user_id(call.from_user.id)

    await db.remove_one_product(user_id,product_id)

    products = await db.get_cart_products(user_id)
    await call.message.answer("Savatchangiz:",
        reply_markup=cart_keyboard(products))
    await call.answer()


@router.callback_query(F.data == "checkout")
async def checkout(call: CallbackQuery,db):
    user_id = await db.get_user_id(call.from_user.id)
    products, total = await db.get_cart_with_total(user_id)

    if not products:
        await call.message.answer("Savatchangiz bo'sh")
        return

    text = "🛒 Buyurtmangiz:\n\n"

    for product in products:
        text += f"•{product['name']} - {product['price']} so'm\n"

    text += f"\n💰 Umumiy narx: {total} so'm"

    await call.message.answer(
        text,
        reply_markup=payment_keyboard()
    )

    await call.answer()

@router.callback_query(F.data == "pay_card")
async def pay_card(call: CallbackQuery,):

    await call.message.answer(
        "💳 To'lov uchun karta:\n"
        "8600 1234 5678 9012\n\n"
        "To'lov qilgandan keyin chek yuboring."
    )
    await call.answer()

    My_id=8023714461

    await call.bot.send_message(chat_id=My_id,text="Assalomu alaykum buyurtmani tasdiqlash uchun lokatsiya tashlang")


@router.message(F.location)
async def location(message: Message):
    latitude = message.location.latitude
    longitude = message.location.longitude

    await message.answer("Lokatsiyangiz,uchun rahmat buyurtmangiz qabul qilindi")
    await message.answer_location(latitude=latitude,longitude=longitude)

@router.callback_query(F.data == "pay_cash")
async def pay_cash(call: CallbackQuery,db):

    user_id = await db.get_user_id(call.from_user.id)
    await db.confirm_order(user_id)

    await call.message.answer(
        "✅ Buyurtmangiz qabul qilindi!\n"
        "Courier yetkazib berganda naqd to'laysiz."
    )
    await call.answer()

@router.message(F.text == "Mening buyurtmalarim",RoleFilter("user"))
async def story_orders(message:Message,db):

    user_id = await db.get_user_id(message.from_user.id)
    orders, total = await db.get_order_history(user_id)

    if not orders:
        await message.answer("📦 Sizda hali buyurtmalar yo'q")
        return

    text = "📦 Buyurtmalar tarixi:\n\n"

    for product in orders:
        text += f"🆔 {product['id']} | {product['name']} - {product['price']} so'm\n"
    
    text +=f"\n💰 Umumiy narx {total} so'm"

    await message.answer(text)