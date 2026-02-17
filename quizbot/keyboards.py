from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    keyboard = [
        [KeyboardButton(text="🎯 Test boshlash")],
        [KeyboardButton(text="➕ Savol qo'shish")],
        [KeyboardButton(text="🗑 Savol o'chirish")],
        [KeyboardButton(text="📊 Natijalar")],
        [KeyboardButton(text="📝 Barcha savollar")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def quiz_options(question_id, options):
    keyboard = [
        [InlineKeyboardButton(text=f"A) {options['a']}", callback_data=f"answer_{question_id}_a")],
        [InlineKeyboardButton(text=f"B) {options['b']}", callback_data=f"answer_{question_id}_b")],
        [InlineKeyboardButton(text=f"C) {options['c']}", callback_data=f"answer_{question_id}_c")],
        [InlineKeyboardButton(text=f"D) {options['d']}", callback_data=f"answer_{question_id}_d")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def delete_keyboard(question_id):
    keyboard = [
        [InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"delete_{question_id}")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_delete")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)