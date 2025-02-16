import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

bot = Bot(token=os.environ.get('GPT_TOKEN'))
dispatch = Dispatcher()

async def start_bot():
    await dispatch.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_bot())