from aiogram import F
from aiogram.types import Message, CallbackQuery
from bot import dp
from config import is_admin
from states import QuizForm
from keyboards import delete_keyboard, main_menu
from db import get_db
from utils import validate_question, validate_option
from aiogram.fsm.context import FSMContext

@dp.message(F.text == "➕ Savol qo'shish")
async def add_q(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return await message.answer("❌ Ruxsat yo`q")
    await message.answer("❓ Savolni kiriting:")
    await state.set_state(QuizForm.question)

@dp.message(QuizForm.question)
async def add_question_text(message: Message, state: FSMContext):
    is_valid, error_msg = validate_question(message.text)
    if not is_valid:
        await message.answer(error_msg + "\n\nIltimos, qaytadan kiriting:")
        return
    await state.update_data(question=message.text)
    await message.answer("📝 A variantini kiriting:")
    await state.set_state(QuizForm.option_a)

@dp.message(QuizForm.option_a)
async def add_option_a(message: Message, state: FSMContext):
    is_valid, error_msg = validate_option(message.text, "A")
    if not is_valid:
        await message.answer(error_msg + "\n\nIltimos, qaytadan kiriting:")
        return
    await state.update_data(option_a=message.text)
    await message.answer("📝 B variantini kiriting:")
    await state.set_state(QuizForm.option_b)

@dp.message(QuizForm.option_b)
async def add_option_b(message: Message, state: FSMContext):
    is_valid, error_msg = validate_option(message.text, "B")
    if not is_valid:
        await message.answer(error_msg + "\n\nIltimos, qaytadan kiriting:")
        return
    await state.update_data(option_b=message.text)
    await message.answer("📝 C variantini kiriting:")
    await state.set_state(QuizForm.option_c)

@dp.message(QuizForm.option_c)
async def add_option_c(message: Message, state: FSMContext):
    is_valid, error_msg = validate_option(message.text, "C")
    if not is_valid:
        await message.answer(error_msg + "\n\nIltimos, qaytadan kiriting:")
        return
    await state.update_data(option_c=message.text)
    await message.answer("📝 D variantini kiriting:")
    await state.set_state(QuizForm.option_d)

@dp.message(QuizForm.option_d)
async def add_option_d(message: Message, state: FSMContext):
    is_valid, error_msg = validate_option(message.text, "D")
    if not is_valid:
        await message.answer(error_msg + "\n\nIltimos, qaytadan kiriting:")
        return
    await state.update_data(option_d=message.text)
    await message.answer("✅ To'g'ri javobni kiriting (a, b, c yoki d):")
    await state.set_state(QuizForm.correct)

@dp.message(QuizForm.correct)
async def add_correct_answer(message: Message, state: FSMContext):
    correct = message.text.lower().strip()
    if correct not in ['a', 'b', 'c', 'd']:
        await message.answer("❌ Faqat a, b, c yoki d harfini kiriting!\n\nQaytadan kiriting:")
        return

    data = await state.get_data()
    options = [data['option_a'], data['option_b'], data['option_c'], data['option_d']]
    if len(set(opt.lower().strip() for opt in options)) < 4:
        await message.answer(
            "❌ Barcha variantlar har xil bo'lishi kerak!\n\n"
            "Savolni qaytadan qo'shish uchun /start bosing."
        )
        await state.clear()
        return

    conn = await get_db()
    await conn.execute(
        """
        INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_answer)
        VALUES ($1, $2, $3, $4, $5, $6)
        """,
        data['question'], data['option_a'], data['option_b'],
        data['option_c'], data['option_d'], correct
    )
    await conn.close()

    await message.answer("✅ Savol muvaffaqiyatli qo'shildi!", reply_markup=main_menu())
    await state.clear()

@dp.message(F.text == "🗑 Savol o'chirish")
async def delete_question_start(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("❌ Ruxsat yo`q")
    conn = await get_db()
    questions = await conn.fetch("SELECT * FROM questions ORDER BY id")
    await conn.close()
    if not questions:
        return await message.answer("Savollar mavjud emas.")

    text = "🗑 O'chirish uchun savolni tanlang:\n\n"
    keyboard = []
    for q in questions:
        short_question = q['question'][:50] + "..." if len(q['question']) > 50 else q['question']
        keyboard.append([
            InlineKeyboardButton(
                text=f"#{q['id']} - {short_question}",
                callback_data=f"show_delete_{q['id']}"
            )
        ])

    keyboard.append([InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_delete")])

    await message.answer(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@dp.callback_query(F.data.startswith("show_delete_"))
async def show_delete_confirmation(callback: CallbackQuery):
    question_id = int(callback.data.split("_")[2])

    conn = await get_db()
    question = await conn.fetchrow("SELECT * FROM questions WHERE id = $1", question_id)
    await conn.close()

    if not question:
        await callback.answer("❌ Savol topilmadi!", show_alert=True)
        return

    text = f"📝 Savol #{question['id']}\n\n"
    text += f"❓ {question['question']}\n\n"
    text += f"A) {question['option_a']}\n"
    text += f"B) {question['option_b']}\n"
    text += f"C) {question['option_c']}\n"
    text += f"D) {question['option_d']}\n"
    text += f"✅ To'g'ri: {question['correct_answer'].upper()}\n\n"
    text += "⚠️ Bu savolni o'chirishni xohlaysizmi?"

    await callback.message.edit_text(
        text,
        reply_markup=delete_keyboard(question_id)
    )

@dp.callback_query(F.data.startswith("delete_"))
async def confirm_delete(callback: CallbackQuery):
    question_id = int(callback.data.split("_")[1])

    conn = await get_db()
    await conn.execute("DELETE FROM questions WHERE id = $1", question_id)
    await conn.close()

    await callback.message.edit_text("✅ Savol muvaffaqiyatli o'chirildi!")
    await callback.answer("✅ O'chirildi!")

@dp.callback_query(F.data == "cancel_delete")
async def cancel_delete(callback: CallbackQuery):
    await callback.message.edit_text("❌ Bekor qilindi")
    await callback.answer()