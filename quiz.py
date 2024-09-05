from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from db import get_quiz_index, update_quiz_index
import json
from db import update_quiz_index, get_quiz_index, update_correct_answers

with open('questions.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)

    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']

    kb = generate_options_keyboard(opts, correct_index)
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

def generate_options_keyboard(answer_options, correct_index):
    builder = InlineKeyboardBuilder()

    for index, option in enumerate(answer_options):
        callback_data = "right_answer" if index == correct_index else "wrong_answer"
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=callback_data
        ))
    builder.adjust(1)
    return builder.as_markup()

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0

    await update_quiz_index(user_id, current_question_index)
    await update_correct_answers(user_id, 0)

    await get_question(message, user_id)
