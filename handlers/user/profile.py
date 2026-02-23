from aiogram import F,Router
from aiogram.types import Message

router=Router()

@router.message(F.text=="Profile")
async def profile(msg:Message,db):
    data= await db.user_profile(msg.from_user.id)
    await msg.answer(f"Profile information: \nIsmingiz: {data['name']} \nYoshingiz: {data['age']} \nTelefon raqam: {data['phone']} \nMansabingiz: {data['role']}")