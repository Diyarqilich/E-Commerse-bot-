import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import config
from handlers.start import router as start_router
from handlers.register import router as register_router
from handlers.user.profile import router as profile_router
from handlers.user.products import router as products_router
from handlers.admin.admin import router as admin_router
from handlers.admin.product import router as admin_product_router


from database.database import Database


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    db = Database()
    await db.connect()

    dp["db"] = db

    dp.include_router(start_router)
    dp.include_router(register_router)
    dp.include_router(profile_router)
    dp.include_router(products_router)
    dp.include_router(admin_router)  
    dp.include_router(admin_product_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())