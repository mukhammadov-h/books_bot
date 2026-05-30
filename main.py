
import asyncio
from aiogram import Bot, Dispatcher
from database import create_tables
import asyncio
import logging
from load import BOT_TOKEN
from basic_handlers import router
logging.basicConfig(level=logging.INFO)



async def main():
  bot = Bot(BOT_TOKEN)
  dp = Dispatcher()
  dp.include_router(router)
  await dp.start_polling(bot)


if __name__ == '__main__':
    create_tables()
    asyncio.run(main())
