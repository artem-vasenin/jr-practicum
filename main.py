import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types

from handlers import command_router

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

async def start_bot():
    bot = Bot(token=os.environ.get('TG_TOKEN'))
    dispatch = Dispatcher()
    dispatch.include_routers(command_router)
    await dispatch.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_bot())