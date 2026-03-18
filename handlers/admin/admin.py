from aiogram import F,Router
from aiogram.types import Message,CallbackQuery
from keyboards.reply import admin_panel_menu, start_reply_admin
from keyboards.inline import users_inline,role_inline
from filters.filter import RoleFilter
from aiogram.fsm.context import FSMContext
from states.ads_states import AdsState
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

@router.message(F.text == "⬅️ Orqaga", RoleFilter("Admin"))
async def back(msg: Message):
    await msg.answer("Orqaga", reply_markup=start_reply_admin())

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

async def broadcasting(bot, users, message):
    success = 0
    failed = 0
    for user_id in users:
        try:

            # Rasm + matn
            if message.photo:
                await bot.send_photo(
                    chat_id=int(user_id["telegram_id"]),
                    photo=message.photo[-1].file_id,
                    caption=message.caption
                )

            # Video + matn
            elif message.video:
                await bot.send_video(
                    chat_id=user_id,
                    video=message.video.file_id,
                    caption=message.caption
                )
            else:
                await bot.send_message(
                    chat_id=user_id,
                    text=message.text
                )

            success += 1

        except Exception:
            failed += 1

    return success, failed

@router.message(F.text == "Reklama", RoleFilter("Admin"))
async def reklama(msg: Message, state: FSMContext):
    
    await msg.answer("📢 Reklama yuborish uchun rasm, video yoki matn yuboring:")
    
    await state.set_state(AdsState.waiting_for_ads)

@router.message(AdsState.waiting_for_ads)
async def reklama(msg:Message,state:FSMContext,db):
    users= await db.get_users_telegram_id()
    message=msg
    success, failed = await broadcasting(
        msg.bot,
        users,
        message
    )

    await msg.answer(
        f"📊 Reklama natijasi:\n"
        f"✅ Yuborildi: {success}\n"
        f"❌ Yuborilmadi: {failed}"
    )
    await state.clear()