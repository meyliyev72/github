from aiogram import F
from aiogram.types import Message
from bot import dp
from db import get_db

@dp.message(F.text == "📊 Natijalar")
async def show_results(message: Message):
    conn = await get_db()

    results = await conn.fetch("""
        SELECT username, score, total, date
        FROM results
        ORDER BY score DESC, date DESC
        LIMIT 10
    """)

    await conn.close()

    if not results:
        await message.answer("📭 Hozircha natijalar yo'q")
        return

    text = "🏆 TOP 10 natijalar\n\n"

    for i, r in enumerate(results, 1):
        percentage = (r['score'] / r['total']) * 100
        text += f"{i}. {r['username']} - {r['score']}/{r['total']} ({percentage:.0f}%)\n"

    await message.answer(text)

@dp.message(F.text == "📝 Barcha savollar")
async def show_all_questions(message: Message):
    conn = await get_db()
    questions = await conn.fetch("select * from questions order by id")
    await conn.close()

    if not questions:
        await message.answer("📭 Hozircha savollar yo'q")