from aiogram import F,Router
from aiogram.types import Message
from filters.filter import RoleFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from states.add_product import AddProductState
from states.update_product import UpdateProductState
from keyboards.inline import inline_action
router=Router()

@router.message(F.text=="➕ Mahsulot qo‘shish",RoleFilter('Admin'))
async def add_product(msg:Message,state:FSMContext):
    await msg.answer("Iltimos mahsulot nomini kiriting!")
    await state.set_state(AddProductState.name)

@router.message(AddProductState.name)
async def add_product(msg:Message,state:FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Iltimos mahsulot narxini kiriting!")
    await state.set_state(AddProductState.price)

@router.message(AddProductState.price)
async def add_product(msg:Message,state:FSMContext):
    await state.update_data(price=msg.text)
    await msg.answer("Iltimos mahsulot tasnifini kiriting!")
    await state.set_state(AddProductState.description)

@router.message(AddProductState.description)
async def add_product(msg:Message,state:FSMContext,db):
    await state.update_data(description=msg.text)

    data=await state.get_data()
    await db.add_product(data["name"],data["price"],data["description"])
    await msg.answer("MMahsulot muvaffaqiyatli qo'shildi")
    await state.clear()

@router.callback_query(F.data.startswith("adminproduct_"),RoleFilter("Admin"))
async def product(call:CallbackQuery):
    product_id = call.data.split("_")[1]
    await call.message.answer("MAhsulotni tahrirlash yoki o'chirish:",reply_markup=inline_action(int(product_id)))
    await call.answer()

@router.callback_query(F.data.startswith("delete_product_"),RoleFilter("Admin"))
async def product(call:CallbackQuery,db):
    product_id = call.data.split("_")[2]
    await db.delete_product(int(product_id))
    await call.message.answer("Mahsulot muvaffaqiyatli o'chirildi!")
    await call.answer()

@router.callback_query(F.data.startswith("edit_product_"),RoleFilter("Admin"))
async def product(call:CallbackQuery,state:FSMContext):
    product_id = int(call.data.split("_")[2])
    await state.set_state(UpdateProductState.product_id)
    await state.update_data(product_id=product_id)
    await call.message.answer("Mahsulotni yangilash uchun nomini kiriting: ")
    await state.set_state(UpdateProductState.name)

@router.message(UpdateProductState.name)
async def product(msg:Message,state:FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Mahsulot narxinini kiriting: ")
    await state.set_state(UpdateProductState.price)

@router.message(AddProductState.price)
async def get_price(message: Message, state: FSMContext):

    if message.text == "⬅️ Orqaga":
        await state.clear()
        await message.answer("Bekor qilindi")
        return

    if not message.text.isdigit():
        await message.answer("Narx faqat raqam bo'lishi kerak!")
        return

    await state.update_data(price=message.text)
    await state.set_state(AddProductState.description)
    await message.answer("Mahsulot tavsifini kiriting:")

@router.message(UpdateProductState.description)
async def product(msg:Message,state:FSMContext,db):
    await state.update_data(description=msg.text)
    data=await state.get_data()
    await db.update_product(
        data["name"],
        data["price"],
        data["description"],
        data["product_id"]
        )
    await msg.answer("Mahsulot muvaffaqiyatli o'zgartirildi!")
    await state.clear()