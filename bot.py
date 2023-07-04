import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from database import sqlite
from config_data.config import load_config
from handlers import user_handlers, other_hanslers, admin_handlers


logger = logging.getLogger(__name__)

async def main():

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    config: Config = load_config(".env")

    storage = MemoryStorage()

    bot: Bot = Bot(
        config.tg_bot.token,
        parse_mode='HTML'
    )
    
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_router(user_handlers.router)
    dp.include_router(admin_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())    