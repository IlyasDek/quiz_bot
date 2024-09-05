import asyncio
from aiogram import Bot, Dispatcher
import logging
from handlers import register_handlers
from db import create_table
from dotenv import load_dotenv
import os


logging.basicConfig(level=logging.INFO)
load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
print("Loaded API token:", API_TOKEN)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def main():
    await create_table()

    register_handlers(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
