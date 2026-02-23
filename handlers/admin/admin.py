from aiogram import F,Router
from aiogram.types import Message,CallbackQuery
from keyboards.reply import admin_panel_menu,start_reply_admin
from keyboards.inline import users_inline,role_inline
from filters.filter import RoleFilter
router=Router()

@router.message(F.text=="Admin panel",RoleFilter("Admin"))
async def admin_panel(msg:Message):
    await msg.answer(f'Admin panelga xush kelibsz',reply_markup=admin_panel_menu())

@router.message(F.text==("👥 Userlar"), RoleFilter("Admin"))
async def show_users(message: Message, db):
    users = await db.get_users()

    if not users:
        await message.answer("Userlar yo‘q")
        return

    await message.answer(
        "👥 Userlar ro‘yxati:",
        reply_markup=users_inline(users)
    )

@router.callback_query(F.data.startswith("user_"),RoleFilter("Admin"))
async def choose_role(callback: CallbackQuery):
    telegram_id = int(callback.data.split("_")[1]) #user_1716549072=> ["user","1716549072"]

    await callback.message.answer(
        "🔄 Role tanlang:",
        reply_markup=role_inline(telegram_id)
    )
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("setrole_"),RoleFilter("Admin"))
async def set_role(callback: CallbackQuery, db):
    _, role, telegram_id = callback.data.split("_")
    await db.set_user_role(
        telegram_id=int(telegram_id),
        role=role
    )

    await callback.message.edit_text(
        f"✅ User roli `{role}` ga o‘zgartirildi"
    )
    await callback.answer("Role yangilandi")

@router.callback_query(lambda c: c.data.startswith("Orqaga"),RoleFilter("Admin"))
async def go_back(callback: CallbackQuery):
    await callback.message.answer("🔙 Orqaga qaytish",reply_markup=start_reply_admin())
    await callback.answer()