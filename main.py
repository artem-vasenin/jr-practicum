import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from handlers import router

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

def on_started():
    print('Bot started')

def on_stopped():
    print('Bot stopped')

async def start_bot():
    bot = Bot(token=os.environ.get('TG_TOKEN'))
    dispatch = Dispatcher()
    dispatch.startup.register(on_started)
    dispatch.shutdown.register(on_stopped)
    dispatch.include_routers(router)
    await dispatch.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        ...