from aiogram.filters import CommandStart
from aiogram.types import Message
from bot import dp
from keyboards import main_menu

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"👋 Salom {message.from_user.first_name}!\n\n"
        "🎯 Quiz test botiga xush kelibsiz!\n"
        "Testni boshlash uchun tugmani bosing.",
        reply_markup=main_menu()
    )