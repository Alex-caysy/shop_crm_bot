import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
import database.db as db
from handlers.user import order, start

logging.basicConfig(level=logging.INFO)

# ВАЖНО: start включаем первым — его хендлеры проверяются раньше
dp = Dispatcher(storage=MemoryStorage())
dp.include_routers(start.router, order.router)


async def main():
    await db.init_db()    # таблицы + тестовые товары

    bot = Bot(token=config.BOT_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    logging.info("Бот запущен")


if __name__ == "__main__":
    asyncio.run(main())
