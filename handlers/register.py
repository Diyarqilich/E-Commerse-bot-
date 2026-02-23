from aiogram import Router,F
from aiogram.types import Message,ReplyKeyboardRemove
from states.register import RegisterState
from aiogram.fsm.context import FSMContext
from keyboards.reply import start_reply

router=Router()

@router.message(F.text=="Register")
async def register_handler(msg:Message,state:FSMContext,db):
    if await db.is_user_exists(msg.from_user.id):
        await msg.answer("Siz allaqachon registratsiyadan o'tib bo'lgansiz",reply_markup=start_reply())
    else:
        await msg.answer("Registratsiyadan o'tish uchun ismingizni kiriting: ")
        await state.set_state(RegisterState.name)

@router.message(RegisterState.name)
async def register_handler(msg:Message,state:FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Familyangizni kiriting: ")
    await state.set_state(RegisterState.surename)

@router.message(RegisterState.surename)
async def register_handler(msg:Message,state:FSMContext):
    await state.update_data(surename=msg.text)
    await msg.answer("Yoshingizni kiriting: ")
    await state.set_state(RegisterState.age)

@router.message(RegisterState.age)
async def register_handler(msg:Message,state:FSMContext):
    await state.update_data(age=msg.text)
    await msg.answer("Raqamingizni  kiriting: ")
    await state.set_state(RegisterState.number)

@router.message(RegisterState.number)
async def register_handler(msg:Message,state:FSMContext,db):
    await state.update_data(number=msg.text)
    
    data=await state.get_data()
    await msg.answer(text=f'Ismingiz: {data['name']}\nFamilyangiz: {data['surename']}\nYoshingiz: {data['age']}\nRaqamingiz: {data['number']}\n')
    await db.add_user(msg.from_user.id,data["name"],data["surename"],data["age"],data["number"])
    await msg.answer("Siz muvafaqqiyatli ro'yxatdan o'tdingiz!",reply_markup=ReplyKeyboardRemove())

    await state.clear()