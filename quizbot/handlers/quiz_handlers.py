from aiogram import F
from aiogram.types import Message, CallbackQuery
from bot import dp
from keyboards import quiz_options
from db import get_db
from config import is_admin
from states import QuizForm
from aiogram.fsm.context import FSMContext

current_quiz = {}
user_scores = {}

@dp.message(F.text == "🎯 Test boshlash")
async def start_quiz(message: Message):
    user_id = message.from_user.id
    user_scores[user_id] = {"correct": 0, "total": 0, "current_index": 0}

    conn = await get_db()
    questions = await conn.fetch("SELECT * FROM questions ORDER BY RANDOM()")
    await conn.close()

    if not questions:
        await message.answer("❌ Hozircha savollar yo'q!")
        return

    current_quiz[user_id] = [dict(q) for q in questions]

    question = current_quiz[user_id][0]
    options = {
        'a': question['option_a'],
        'b': question['option_b'],
        'c': question['option_c'],
        'd': question['option_d']
    }

    await message.answer(
        f"❓ Savol 1/{len(current_quiz[user_id])}\n\n"
        f"{question['question']}",
        reply_markup=quiz_options(question['id'], options)
    )

@dp.callback_query(F.data.startswith("answer_"))
async def check_answer(callback: CallbackQuery):
    user_id = callback.from_user.id
    parts = callback.data.split("_")
    question_id = int(parts[1])
    user_answer = parts[2]

    if user_id not in current_quiz:
        await callback.answer("❌ Testni qaytadan boshlang!")
        return

    current_index = user_scores[user_id]["current_index"]
    question = current_quiz[user_id][current_index]

    user_scores[user_id]["total"] += 1

    if user_answer == question['correct_answer']:
        user_scores[user_id]["correct"] += 1
        await callback.answer("✅ To'g'ri javob!", show_alert=True)
    else:
        await callback.answer(
            f"❌ Noto'g'ri! To'g'ri javob: {question['correct_answer'].upper()}",
            show_alert=True
        )

    user_scores[user_id]["current_index"] += 1

    if user_scores[user_id]["current_index"] >= len(current_quiz[user_id]):
        score = user_scores[user_id]["correct"]
        total = user_scores[user_id]["total"]
        percentage = (score / total) * 100

        conn = await get_db()
        await conn.execute(
            """
            INSERT INTO results (user_id, username, score, total, date, time)
            VALUES ($1, $2, $3, $4, CURRENT_DATE, CURRENT_TIME)
            """,
            user_id, callback.from_user.username or callback.from_user.first_name,
            score, total
        )
        await conn.close()

        result_text = f"🏁 Test yakunlandi!\n\n"
        result_text += f"✅ To'g'ri javoblar: {score}\n"
        result_text += f"❌ Noto'g'ri javoblar: {total - score}\n"
        result_text += f"📊 Natija: {percentage:.1f}%\n\n"

        if percentage >= 80:
            result_text += "🏆 A'lo natija!"
        elif percentage >= 60:
            result_text += "👍 Yaxshi natija!"
        else:
            result_text += "📚 Ko'proq mashq qiling!"

        await callback.message.edit_text(result_text)

        del current_quiz[user_id]
        del user_scores[user_id]
        return

    next_question = current_quiz[user_id][user_scores[user_id]["current_index"]]
    options = {
        'a': next_question['option_a'],
        'b': next_question['option_b'],
        'c': next_question['option_c'],
        'd': next_question['option_d']
    }

    await callback.message.edit_text(
        f"❓ Savol {user_scores[user_id]['current_index'] + 1}/{len(current_quiz[user_id])}\n\n"
        f"{next_question['question']}",
        reply_markup=quiz_options(next_question['id'], options)
    )