import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

from handlers import *

async def main():
    print("🤖 Quiz bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())