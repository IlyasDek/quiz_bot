from aiogram import Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
from quiz import quiz_data, get_question
from db import update_quiz_index, update_correct_answers, get_user_stats, get_quiz_index

def register_handlers(dp: Dispatcher):
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        builder = ReplyKeyboardBuilder()
        builder.add(types.KeyboardButton(text="Начать игру"))
        builder.add(types.KeyboardButton(text="Статистика"))
        await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

    @dp.message(F.text == "Начать игру")
    @dp.message(Command("quiz"))
    async def cmd_quiz(message: types.Message):
        await message.answer(f"Давайте начнем квиз!")
        await new_quiz(message)

    @dp.message(F.text == "Статистика")
    async def cmd_stats(message: types.Message):
        user_id = message.from_user.id
        stats = await get_user_stats(user_id)
        if stats is not None:
            await message.answer(f"Ваш последний результат: {stats} правильных ответов")
        else:
            await message.answer("Вы еще не проходили квиз")

    @dp.callback_query(F.data.startswith("right_answer"))
    async def right_answer(callback: types.CallbackQuery):
        user_id = callback.from_user.id

        correct_answers = await get_user_stats(user_id) or 0
        correct_answers += 1
        await update_correct_answers(user_id, correct_answers)  # Обновляем в базе данных

        await callback.bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None
        )
        await callback.message.answer("Верно!")

        current_question_index = await get_quiz_index(user_id)
        current_question_index += 1
        await update_quiz_index(user_id, current_question_index)

        if current_question_index < len(quiz_data):
            await get_question(callback.message, user_id)
        else:
            await callback.message.answer(f"Это был последний вопрос. Квиз завершен! Правильных ответов: {correct_answers}")

    @dp.callback_query(F.data.startswith("wrong_answer"))
    async def wrong_answer(callback: types.CallbackQuery):
        user_id = callback.from_user.id

        await callback.bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None
        )
        await callback.message.answer("Неправильно.")

        current_question_index = await get_quiz_index(user_id)
        correct_option = quiz_data[current_question_index]['correct_option']
        await callback.message.answer(f"Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

        current_question_index += 1
        await update_quiz_index(user_id, current_question_index)

        if current_question_index < len(quiz_data):
            await get_question(callback.message, user_id)
        else:
            await callback.message.answer(f"Это был последний вопрос. Квиз завершен!")

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await update_correct_answers(user_id, 0)
    await get_question(message, user_id)
